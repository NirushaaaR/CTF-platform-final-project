# Generated by Django 3.1.3 on 2021-01-08 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_auto_20201225_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='challengeflag',
            name='explanation',
            field=models.CharField(default='explain', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='challengeflag',
            name='name',
            field=models.CharField(default='name', max_length=255),
            preserve_default=False,
        ),
    ]
