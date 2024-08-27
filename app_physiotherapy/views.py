from django.shortcuts import render, redirect
from .models import User, Scheduler


# Rotas públicas
def home(request):
    return render(request, 'users/home.html')

def login(request):
    return render(request, 'users/login.html')

def register(request):
    return render(request, 'users/register.html' )

# Registra usuários
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

# Faz login e verificar se o usuário é profissional ou paciente.
def login_users(request):
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
        #tratamento de erro
        return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})

# return render(request,'users/users.html', {'users': users}) # o terceiro argumento sempre tem que ser um objeto

# Criação de agendamento
def create_schedule(request):
    # Pega o nome do usuário logado passado pela função login_users
    name_logado = request.session.get('user_name')
    user = User.objects.filter(name=name_logado, type_user="paciente").first()
    
    scheduler = Scheduler.objects.all()
    
    if request.method == 'POST':
        if user:
            # Cria um novo agendamento
            new_scheduler = Scheduler()
            new_scheduler.name = request.POST.get('paciente_name')
            new_scheduler.date = request.POST.get('data')
            new_scheduler.hourly = request.POST.get('horario')
            new_scheduler.doctor = request.POST.get('doutor')
            new_scheduler.extra = request.POST.get('info_extra')
            new_scheduler.save()

            # Repassa os dados do agendamento para o template
            context = {
                'schedulers': scheduler,
                'paciente_name': new_scheduler.name,
                'data': new_scheduler.date,
                'horario': new_scheduler.hourly,
                'doutor': new_scheduler.doctor,
                'info_extra': new_scheduler.extra,
                'users': user,
            }
            
            return render(request, 'users/create_schedule.html', context)
        else:
            return render(request, 'error.html', {'error': 'Usuário não encontrado'})
    
    # Para requisições GET, exibe o formulário de agendamento
    return render(request, 'users/create_schedule.html', {'schedulers': scheduler, 'users': user})
    
    # Para requisições GET, exibe o formulário de agendamento
