from lib.models import Genre, Collection, Library, User, InstanceBook, Books, LectureGroup, Lecturer


def extras(request):
    libraries = Library.objects.all()
    genre = Genre.objects.all()
    collection = Collection.objects.all()
    users = User.objects.all().order_by('-date_joined')
    books = Books.objects.all()
    instances = InstanceBook.objects.all()
    lecture_group = LectureGroup.objects.all()
    lecturer = Lecturer.objects.all()

    return {
        'context_libraries': libraries,
        'context_genre': genre,
        'context_collection': collection,
        'context_users': users,
        'context_books': books,
        'context_instances': instances,
        'context_lecture_group': lecture_group,
        'context_lecturer': lecturer,
    }