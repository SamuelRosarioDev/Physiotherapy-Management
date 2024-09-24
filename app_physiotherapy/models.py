from django.db import models

class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(default='example@example.com')
    age = models.IntegerField()
    password = models.CharField(max_length=128)
    type_user = models.CharField(max_length=50) 

    def __str__(self):
        return self.name


class Scheduler(models.Model):
    STATUS_CHOICES = [('pagar', 'Pagar'), ('pago', 'Pago')]

    status = models.CharField(max_length=20, default='pagar', choices=STATUS_CHOICES) 
    name = models.TextField(max_length=10)
    date = models.DateField()
    hourly = models.TimeField()
    doctor = models.TextField()
    age = models.TextField()
    progress = models.TextField(default='Consulta')
    value = models.DecimalField(max_digits=6, decimal_places=2, default=100)
