from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Scheduler
from django.core.exceptions import ValidationError

# Rotas públicas
def home(request):
    return render(request, 'users/home.html')

def login(request):
    return render(request, 'users/login.html')

def register(request):
    return render(request, 'users/register.html' )

def create_users(request):
    # Salva informações da tela e envia para o banco de dados SQLite
    if request.method == 'POST':
        new_user = User()
        new_user.name = request.POST.get('nome')
        new_user.email = request.POST.get('email')
        new_user.age = request.POST.get('idade')
        new_user.password = request.POST.get('senha')
        new_user.type_user = request.POST.get('tipo_de_usuario')
        new_user.save()
    return render(request,'users/register.html')

def login_users(request):
    # Login
    name = request.POST.get('nome')
    password = request.POST.get('senha')
    
    user = User.objects.filter(name=name, password=password).first()
    
    if user:
        request.session['user_name'] = user.name
        if user.type_user == "profissional":
            return render(request, 'users/page_professional.html')
        elif user.type_user == "paciente": 
            return render(request, 'users/page_patient.html')
    else:
        return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})

def create_schedule(request):
    # Cria agendamento
    name_logado = request.session.get('user_name')
    user = User.objects.filter(name=name_logado, type_user="paciente").first()
    profissionais = User.objects.filter(type_user="profissional")
    
    progress_options = [
        {'progress': 'Consulta', 'valor': 100},
        {'progress': 'Sessão de fisioterapia', 'valor': 150},
        {'progress': 'Revisão', 'valor': 120},
    ]
    
    if request.method == 'POST':
        if user:
            
            new_scheduler = Scheduler()
            new_scheduler.status = "pagar"
            new_scheduler.name = request.POST.get('paciente_name')
            new_scheduler.date = request.POST.get('data')
            new_scheduler.hourly = request.POST.get('horario')
            new_scheduler.doctor = request.POST.get('doutor')
            new_scheduler.age = request.POST.get('age')
            new_scheduler.progress = 'Consulta'
            new_scheduler.value = 100
            
            new_scheduler.save()

            return redirect('create_schedule')

        else:
            return render(request, 'error.html', {'error': 'Usuário não encontrado'})
    
    if user:
        scheduler = Scheduler.objects.filter(name=user.name)
    else:
        scheduler = Scheduler.objects.none()
    
    context = {
        'schedulers': scheduler,
        'users': user,
        'profissionais': profissionais,
        'progress_options': progress_options,
    }
    
    return render(request, 'users/create_schedule.html', context)

def delete_schedule(request, id):
    # Deleta agendamento
    scheduler = get_object_or_404(Scheduler, id=id)
    
    name_logado = request.session.get('user_name')
    user = User.objects.filter(name=name_logado).first()

    if request.method == 'POST':
   
        if user and (user.type_user in ["profissional", "paciente"]):
            scheduler.delete()
            
     
            if user.type_user == "profissional":
                return redirect('list_sessions')
            else: 
                return redirect('create_schedule')
        else:
            return redirect('error_page') 

    return redirect('error_page')


def payment_page(request):
    # Carrega a tela de pagamento
    name_logado = request.session.get('user_name')
    
    user = User.objects.filter(name=name_logado).first()
    
    if user:
        pending_payments = Scheduler.objects.filter(name=name_logado)
    else:
        pending_payments = Scheduler.objects.none()
    
    return render(request, 'users/payment_page.html', {'pending_payments': pending_payments})

def mark_as_paid(request, id):
    # Faz o pagamento
    scheduler = get_object_or_404(Scheduler, id=id)
    if request.method == 'POST':
        scheduler.status = "pago"
        scheduler.save()
        return redirect('payment_page')  
    
    return render(request, 'error.html', {'error': 'Método não permitido'})

def list_sessions(request):
    # Lista de agendamentos
    name_logado = request.session.get('user_name')
    
    user = User.objects.filter(name=name_logado).first()
    
    if user and user.type_user == "profissional":
        sessions = Scheduler.objects.filter(doctor=name_logado)
    else:
        sessions = Scheduler.objects.none()
    
    return render(request, 'users/list_sessions.html', {'sessions': sessions})

def progress_session(request):
    # atualiza o progresso
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        new_date = request.POST.get('new_date')
        new_time = request.POST.get('new_time')

        # Verifique se os campos de data e hora foram preenchidos corretamente
        if not new_date or not new_time:
            return render(request, 'users/list_sessions.html', {
                'sessions': Scheduler.objects.all(),
                'error': 'Data e hora são obrigatórios'
            })

        session = get_object_or_404(Scheduler, id=session_id)

        # Atualize a data e hora da sessão
        session.date = new_date
        session.hourly = new_time

        progress_map = {
            'Consulta': ('Sessão de fisioterapia', 150),
            'Sessão de fisioterapia': ('Revisão', 120)
        }

        if session.progress in progress_map:
            session.progress, session.value = progress_map[session.progress]
            session.status = "pagar"
        elif session.progress == 'Revisão' and session.status == 'pago':
            session.delete()
            return redirect('list_sessions')
        else:
            session.status = "pagar"

        try:
            session.save()
        except ValidationError as e:
            return render(request, 'users/list_sessions.html', {
                'sessions': Scheduler.objects.all(),
                'error': str(e)
            })

    return redirect('list_sessions')
