# Generated by Django 5.1 on 2024-08-26 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_physiotherapy', '0007_alter_user_type_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type_user',
            field=models.TextField(),
        ),
    ]
