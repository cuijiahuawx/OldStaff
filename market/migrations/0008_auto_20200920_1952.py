# Generated by Django 3.1.1 on 2020-09-20 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0007_remove_good_介绍'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='价格',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
