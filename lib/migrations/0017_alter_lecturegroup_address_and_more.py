# Generated by Django 4.1.3 on 2022-12-13 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0016_userdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturegroup',
            name='address',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='library',
            name='address_city',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='library',
            name='address_country',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='library',
            name='address_name',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='library',
            name='address_zip_code',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(max_length=500),
        ),
    ]