from lib.models import UserData, Genre, Collection, Library, User, InstanceBook, Books, LectureGroup, Lecturer, Forum


def extras(request):
    libraries = Library.objects.all()
    genre = Genre.objects.all()
    collection = Collection.objects.all()
    users = User.objects.all().order_by('-date_joined')
    userdata = UserData.objects.all()
    books = Books.objects.all()
    instances = InstanceBook.objects.all()
    lecture_group = LectureGroup.objects.all()
    lecturer = Lecturer.objects.all()
    forum = Forum.objects.all()

    return {
        'context_libraries': libraries,
        'context_genre': genre,
        'context_collection': collection,
        'context_users': users,
        'context_user_data': userdata,
        'context_books': books,
        'context_instances': instances,
        'context_lecture_group': lecture_group,
        'context_lecturer': lecturer,
        'context_forums': forum,
    }