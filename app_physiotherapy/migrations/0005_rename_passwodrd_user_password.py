# Generated by Django 5.1 on 2024-08-25 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_physiotherapy', '0004_rename_password_user_passwodrd'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='passwodrd',
            new_name='password',
        ),
    ]
