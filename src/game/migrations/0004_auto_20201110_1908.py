# Generated by Django 3.1.3 on 2020-11-10 12:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_challenge_flag_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='userchallengerecord',
            name='answered_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userparticipategame',
            name='game_score',
            field=models.IntegerField(default=0),
        ),
    ]
