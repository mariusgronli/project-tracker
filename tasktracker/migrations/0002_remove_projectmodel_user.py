# Generated by Django 3.0.3 on 2020-05-29 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasktracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectmodel',
            name='user',
        ),
    ]
