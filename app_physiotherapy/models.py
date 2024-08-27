from django.db import models

class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    name = models.TextField(max_length=10)
    email = models.EmailField(default='example@example.com')
    age = models.IntegerField()
    password = models.TextField()
    type_user = models.TextField()

class Scheduler (models.Model):
    name = models.TextField(max_length=10)
    date = models.DateField()
    hourly = models.TimeField()
    doctor = models.TextField()
    extra = models.TextField()
    
    