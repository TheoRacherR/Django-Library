# Generated by Django 4.1.3 on 2022-12-09 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0011_alter_instancebook_borrowing_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LectureGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('title', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=500)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='lecturer',
            name='id_lg',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lib.lecturegroup'),
        ),
        migrations.DeleteModel(
            name='LectureGroupe',
        ),
    ]
