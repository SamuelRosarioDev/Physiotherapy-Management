# Generated by Django 5.1 on 2024-08-27 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_physiotherapy', '0008_alter_user_type_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=10)),
                ('date', models.DateField()),
                ('hourly', models.TimeField()),
                ('doctor', models.TextField()),
                ('extra', models.TextField()),
            ],
        ),
    ]
