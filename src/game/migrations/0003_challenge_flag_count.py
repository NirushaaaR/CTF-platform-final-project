# Generated by Django 3.1.3 on 2020-11-09 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20201109_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='flag_count',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
