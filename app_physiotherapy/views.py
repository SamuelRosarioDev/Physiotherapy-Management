from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from .models import User, Scheduler
from .forms import SchedulerForm, CustomUserForm


class HomeView(TemplateView):
    template_name = 'users/home.html'

class LoginView(TemplateView):
    template_name = 'users/login.html'

    def post(self, request):
        name = request.POST.get('nome')
        password = request.POST.get('senha')
        
        user = User.objects.filter(name=name, password=password).first()
        
        if user:
            request.session['user_name'] = user.name
            if user.type_user == "profissional":
                template_name = 'users/page_professional.html'
                return render(request, template_name)
            elif user.type_user == "paciente":
                template_name = 'users/page_patient.html'
                return render(request, template_name)
        else:
            return render(request, self.template_name, {'error': 'Usuário ou senha inválidos'})

class UserCreateView(CreateView):
    model = User
    form_class = CustomUserForm
    fields = ['name', 'email', 'age', 'password', 'type_user']
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        return super().form_valid(form)
    
class SchedulerCreateView(CreateView):
    model = Scheduler
    form_class = SchedulerForm
    template_name = 'users/create_schedule.html'
    success_url = reverse_lazy('payment_page')

class SchedulerCreateView(CreateView):
    model = Scheduler
    form_class = SchedulerForm
    template_name = 'users/create_schedule.html'
    success_url = reverse_lazy('payment_page') 

    def form_valid(self, form):
        form.instance.status = "pagar"
        form.instance.progress = "Consulta" 
        form.instance.value = 100.00 
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        name_logado = self.request.session.get('user_name')
        user = User.objects.filter(name=name_logado).first()
        if user:
            initial['name'] = user.name
            initial['age'] = user.age
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name_logado = self.request.session.get('user_name')
        context['users'] = User.objects.filter(name=name_logado, type_user="paciente").first()
        context['profissionais'] = User.objects.filter(type_user="profissional")
        context['progress_options'] = [
            {'progress': 'Consulta', 'valor': 100},
            {'progress': 'Sessão de fisioterapia', 'valor': 150},
            {'progress': 'Revisão', 'valor': 120},
        ]
        return context

class SessionListView(ListView):
    model = Scheduler
    template_name = 'users/list_sessions.html'
    success_url = reverse_lazy('list_sessions')  

    context_object_name = 'sessions'

    def get_queryset(self):
        name_logado = self.request.session.get('user_name')
        user = User.objects.filter(name=name_logado).first()
        if user and user.type_user == "profissional":
            return Scheduler.objects.filter(doctor=name_logado)
        return Scheduler.objects.none()

class SchedulerDeleteView(DeleteView):
    model = Scheduler
    template_name = 'users/confirm_delete.html'
    success_url = reverse_lazy('list_sessions') 

    def get_queryset(self):
        name_logado = self.request.session.get('user_name')
        user = User.objects.filter(name=name_logado).first()

        if user and (user.type_user == "profissional" or user.type_user == "paciente"):
            return Scheduler.objects.filter(id=self.kwargs['pk'])

        return Scheduler.objects.none()

    def get_success_url(self):
        name_logado = self.request.session.get('user_name')
        user = User.objects.filter(name=name_logado).first()

        if user and user.type_user == "profissional":
            return reverse_lazy('list_sessions')
        else:
            return reverse_lazy('payment_page') 

class MarkAsPaidView(UpdateView):
    model = Scheduler
    fields = []
    template_name = 'users/mark_as_paid.html'
    success_url = reverse_lazy('payment_page')

    def form_valid(self, form):
        form.instance.status = 'pago'
        return super().form_valid(form)

class PaymentPageView(ListView):
    model = Scheduler
    template_name = 'users/payment_page.html'
    context_object_name = 'pending_payments'

    def get_queryset(self):
        name_logado = self.request.session.get('user_name')
        return Scheduler.objects.filter(name=name_logado)


class ProgressSessionView(UpdateView):
    model = Scheduler
    fields = ['date', 'hourly'] 
    template_name = 'path/to/your/template.html'
    success_url = reverse_lazy('list_sessions')

    def form_valid(self, form):
        # Obtenha a sessão atual
        session = form.save(commit=False)

        if session.progress == 'Consulta':
            session.progress = 'Sessão de fisioterapia'
            session.value = 150  
        elif session.progress == 'Sessão de fisioterapia':
            session.progress = 'Revisão'
            session.value = 120  
        else:
            pass
        
        session.status = 'pagar'
        session.save()
        
        return super().form_valid(form)