# Generated by Django 4.1.3 on 2022-12-07 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0008_instancebooks_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instancebooks',
            name='test',
        ),
    ]
