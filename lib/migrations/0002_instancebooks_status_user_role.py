# Generated by Django 4.1.3 on 2022-11-18 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instancebooks',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.IntegerField(default=0),
        ),
    ]
