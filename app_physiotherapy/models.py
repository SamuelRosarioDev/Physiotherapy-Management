from django.db import models

class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    name = models.TextField(max_length=10)
    email = models.EmailField(default='example@example.com')
    age = models.IntegerField()
    password = models.TextField()
    type_user = models.TextField()

class Scheduler (models.Model):
    STATUS_CHOICES = [('pagar', 'Pagar'), ('pago', 'Pago')]
    
    status = models.CharField(max_length=20, default='pending', choices=STATUS_CHOICES)
    name = models.TextField(max_length=10)
    date = models.DateField()
    hourly = models.TimeField()
    doctor = models.TextField()
    age = models.TextField()
    progress = models.TextField(default='Consulta')
    value = models.TextField(default=100)

