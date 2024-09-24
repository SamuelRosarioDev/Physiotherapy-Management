from django import forms
from .models import User, Scheduler

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['name', 'email', 'age', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class SchedulerForm(forms.ModelForm):
    class Meta:
        model = Scheduler
        fields = ['name', 'date', 'hourly', 'doctor', 'age']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), 
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hourly': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),  
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'] = forms.ModelChoiceField(
            queryset=User.objects.filter(type_user='profissional'),
            empty_label="Selecione um médico",
            widget=forms.Select(attrs={'class': 'form-control'})
        )
