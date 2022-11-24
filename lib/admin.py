from django.contrib import admin
from .models import (People, Library, Librarian, Collection, Genre, Books, InstanceBooks, LectureGroupe, Lecturer, Forum, Message)


admin.site.register(People)
admin.site.register(Library)
admin.site.register(Librarian)
admin.site.register(Collection)
admin.site.register(Genre)
admin.site.register(Books)
admin.site.register(InstanceBooks)
admin.site.register(LectureGroupe)
admin.site.register(Lecturer)
admin.site.register(Forum)
admin.site.register(Message)