# Generated by Django 4.1.3 on 2022-12-12 08:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lib', '0014_remove_lecturegroup_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturegroup',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]