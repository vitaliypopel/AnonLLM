# Generated by Django 5.0.4 on 2024-05-07 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='answer',
            field=models.CharField(max_length=100000),
        ),
        migrations.AlterField(
            model_name='message',
            name='question',
            field=models.CharField(max_length=20000),
        ),
    ]
