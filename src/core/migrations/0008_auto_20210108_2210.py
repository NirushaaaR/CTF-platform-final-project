# Generated by Django 3.1.3 on 2021-01-08 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210105_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
