# Generated by Django 3.0.7 on 2020-07-08 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='good',
            name='分类',
        ),
        migrations.AddField(
            model_name='good',
            name='分类',
            field=models.ManyToManyField(to='market.Catgory'),
        ),
    ]