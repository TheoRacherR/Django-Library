from django.contrib import admin
from .models import (Library, Librarian, Collection, Genre, Books, InstanceBook, LectureGroup, Lecturer, Forum, Message, LectureGroupDetails)

class LibrarianAdmin(admin.ModelAdmin):
    list_display = ("id_user", "id_library")

class InstanceAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'id_books', 'id_library', 'borrowing_date', 'max_date', 'status')

class LecturerAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'id_lg')


    


admin.site.register(Library)
admin.site.register(Librarian, LibrarianAdmin)
admin.site.register(Collection)
admin.site.register(Genre)
admin.site.register(Books)
admin.site.register(InstanceBook, InstanceAdmin)
admin.site.register(LectureGroup)
admin.site.register(Lecturer, LecturerAdmin)
admin.site.register(Forum)
admin.site.register(Message)
admin.site.register(LectureGroupDetails)

