# Generated by Django 3.0.7 on 2020-09-19 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_auto_20200919_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='good',
            name='介绍',
        ),
    ]
