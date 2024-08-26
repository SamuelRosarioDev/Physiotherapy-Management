from django.shortcuts import render
from .models import User

def home(request):
    return render(request, 'users/home.html')

def login(request):
    return render(request, 'users/login.html')

def register(request):
    return render(request, 'users/register.html' )

# Forms que executa essa função /register
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

    name = request.POST.get('nome')
    password = request.POST.get('senha')
    
    user = User.objects.filter(name=name, password=password).first()
    if user and user.type_user == "profissional":
        print(user.type_user)
        return render(request, 'users/page_professional.html')
    elif user and user.type_user == "paciente": 
        print(user.type_user)
        return render(request, 'users/page_patient.html')
 # o terceiro argumento sempre tem que ser um objeto


#  return render(request,'users/users.html', {'users': users}) # o terceiro argumento sempre tem que ser um objeto