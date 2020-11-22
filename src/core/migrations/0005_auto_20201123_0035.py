# Generated by Django 3.1.3 on 2020-11-22 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docker_instance', '0001_initial'),
        ('core', '0004_scorehistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='docker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rooms', to='docker_instance.dockerweb'),
        ),
        migrations.AddField(
            model_name='task',
            name='docker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='docker_instance.dockerweb'),
        ),
    ]
