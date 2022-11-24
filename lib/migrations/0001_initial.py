# Generated by Django 4.1.3 on 2022-11-18 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('url_image', models.CharField(max_length=500)),
                ('publisher', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='LectureGroupe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address_name', models.CharField(max_length=500)),
                ('address_city', models.CharField(max_length=500)),
                ('address_country', models.CharField(max_length=500)),
                ('address_zip_code', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('id_forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lib.forum')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lib.user')),
            ],
        ),
        migrations.CreateModel(
            name='Librarian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_library', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lib.library')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lib.user')),
            ],
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_lg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lib.lecturegroupe')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lib.user')),
            ],
        ),
        migrations.CreateModel(
            name='InstanceBooks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_books', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lib.books')),
                ('id_library', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lib.library')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lib.user')),
            ],
        ),
        migrations.AddField(
            model_name='books',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lib.collection'),
        ),
        migrations.AddField(
            model_name='books',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='lib.genre'),
        ),
    ]
