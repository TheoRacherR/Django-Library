from django.db import models

class People(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, default=None)
    password = models.CharField(max_length=200, default=None)
    role = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)


class Library(models.Model):
    name = models.CharField(max_length=200)
    address_name = models.CharField(max_length=500)
    address_city = models.CharField(max_length=500)
    address_country = models.CharField(max_length=500)
    address_zip_code = models.CharField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

class Librarian(models.Model):
    id_user = models.ForeignKey(People, on_delete=models.CASCADE)
    id_library = models.ForeignKey(Library, on_delete=models.CASCADE)

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

class InstanceBooks(models.Model):
    id_user = models.ForeignKey(People, on_delete=models.RESTRICT)
    id_books = models.ForeignKey(Books, on_delete=models.CASCADE)
    id_library = models.ForeignKey(Library, on_delete=models.RESTRICT)
    borrowing_date = models.DateTimeField
    max_date = models.DateTimeField
    status = models.IntegerField(default=0)

class LectureGroupe(models.Model):
    date = models.DateField
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

class Lecturer(models.Model):
    id_user = models.ForeignKey(People, on_delete=models.CASCADE)
    id_lg = models.ForeignKey(LectureGroupe, on_delete=models.CASCADE)

class Forum(models.Model):
    title = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

class Message(models.Model):
    id_user = models.ForeignKey(People, on_delete=models.RESTRICT)
    id_forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)