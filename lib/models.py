from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin

class Library(models.Model):
    # id_user = models.ManyToManyField(User)
    name = models.CharField(max_length=200)
    address_name = models.CharField(max_length=500)
    address_city = models.CharField(max_length=500)
    address_country = models.CharField(max_length=500)
    address_zip_code = models.CharField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

class Librarian(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE) #added
    id_library = models.ForeignKey(Library, on_delete=models.CASCADE) #added


class Collection(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

class Genre(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

class Books(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.RESTRICT)
    genre = models.ForeignKey(Genre, on_delete=models.RESTRICT)
    title = models.CharField(max_length=200) 
    author = models.CharField(max_length=200)
    url_image = models.CharField(max_length=500)
    publisher = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

class InstanceBook(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    id_books = models.ForeignKey(Books, on_delete=models.CASCADE)
    id_library = models.ForeignKey(Library, on_delete=models.RESTRICT)
    borrowing_date = models.DateField(null=True, blank=True)
    max_date = models.DateField(null=True, blank=True)
    status = models.IntegerField(default=0)


class LectureGroup(models.Model):
    # id_user = models.ManyToManyField(User)
    owner = models.ForeignKey(User, on_delete=models.RESTRICT)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

class Lecturer(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE) #added
    id_lg = models.ForeignKey(LectureGroup, on_delete=models.CASCADE) #added

class LectureGroupDetails(models.Model):
    id_lg = models.ForeignKey(LectureGroup, on_delete=models.CASCADE)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()


class Forum(models.Model):
    title = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

class Message(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.RESTRICT)
    id_forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

# class User(AbstractUser):
    # id_lg = models.ManyToManyField(LectureGroup)
    # id_library = models.ManyToManyField(Library)
