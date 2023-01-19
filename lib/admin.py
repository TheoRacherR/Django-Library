from django.contrib import admin
from .models import (UserData, Library, Librarian, Collection, Genre, Books, InstanceBook, LectureGroup, Lecturer, Forum, Message, LectureGroupDetails)

class LibrarianAdmin(admin.ModelAdmin):
    list_display = ("id", "id_user", "id_library")    

class InstanceAdmin(admin.ModelAdmin):
    list_display = ("id", 'id_user', 'id_books', 'id_library', 'borrowing_date', 'max_date', 'status')

class LecturerAdmin(admin.ModelAdmin):
    list_display = ("id", 'id_user', 'id_lg')

class LibraryAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'address_name','address_city','address_country','address_zip_code','creation_date', 'modification_date')

class CollectionAdmin(admin.ModelAdmin):
    list_display = ("id", 'name','creation_date', 'modification_date')

class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", 'name','creation_date', 'modification_date')

class BooksAdmin(admin.ModelAdmin):
    list_display = ("id", 'collection', 'genre', 'title', 'author', 'url_image', 'publisher', 'creation_date', 'modification_date')

class LectureGroupAdmin(admin.ModelAdmin):
    list_display = ("id", 'owner', 'title', 'address','creation_date', 'modification_date')

class ForumAdmin(admin.ModelAdmin):
    list_display= ("id", 'title','creation_date', 'modification_date')

class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", 'id_user', 'id_forum', 'text', 'creation_date', 'modification_date')

class UserDataAdmin(admin.ModelAdmin):
    list_display = ("id", 'user', 'role')



admin.site.register(Library, LibraryAdmin)
admin.site.register(Librarian, LibrarianAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Books, BooksAdmin)
admin.site.register(InstanceBook, InstanceAdmin)
admin.site.register(LectureGroup, LectureGroupAdmin)
admin.site.register(Lecturer, LecturerAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(LectureGroupDetails)
admin.site.register(UserData, UserDataAdmin)

