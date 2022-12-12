from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.template import Context, RequestContext
from django.db import IntegrityError

from .models import Books, Genre, Collection, InstanceBook, Library, Librarian, LectureGroup, Lecturer, LectureGroupDetails
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

from rolepermissions.roles import assign_role

import datetime


#site
def index(request):
    return render(request, "lib/index.html")

#admin
def admin(request):
    return render(request, 'admin/index.html')

def not_founded(request):
    return redirect('/lib/404')


##Auth
#site
def login_def(request):
    
    if request.user.is_authenticated:
            messages.info(request, 'You are already logged in')
            return redirect('/lib/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/lib/')
        else:
            messages.error(request, 'Something wrong happened, try again')
            return redirect('/lib/login/')

    else:
        return render(request, 'lib/auth/login.html')

def signin_def(request):
    try:
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in')
            return redirect('/lib/')

        if request.method == 'POST':
            
            user_admin = User.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password']
            )
            user_admin.save()
            assign_role(user_admin, 'customer')
            messages.success(request, 'User created')

            librarian = Librarian()
            librarian.id_user = user_admin
            lib = Library.objects.get(pk=4)
            librarian.id_library = lib
            librarian.save()


            user_auth = authenticate(request, username=request.POST['username'], password=request.POST['password'])

            login(request, user_auth)
            messages.success(request, 'Logged in')

            return redirect('/lib/')

        else:
            return render(request, 'lib/auth/signin.html')
    except IntegrityError:
        messages.error(request, 'This username already exist')
        return render(request, 'lib/auth/signin.html')

def logout_def(request):
    logout(request)
    return redirect('/lib/')


##Book
#site
def details_book(request, id):
    try:
        book = Books.objects.get(pk=id)
        instances = InstanceBook.objects.filter(id_books=id)

    except Books.DoesNotExist or InstanceBook.DoesNotExist:
        return render(request, 'lib/404.html')

    return render(request, "lib/book/details_book.html", {
        "book": book,
        "instances": instances
    })

def list_books(request, idL, idC, idG):
    # try:

    if request.method == 'POST':
        collec = Collection.objects.get(pk=request.POST["collection"])
        gen = Genre.objects.get(pk=request.POST["genre"])
        books = Books.objects.filter(genre=gen, collection=collec)

        search = "Collection: '" + collec.name + "' and genre: '" + gen.name + "'"

    else:

        if idL != 0:
            library = Library.objects.get(pk=idL)
            lib = InstanceBook.objects.filter(id_library=library)
            list_b = []
            for l in lib:
                if l.id_books not in list_b:
                    list_b.append(l.id_books.pk)
            books = Books.objects.filter(id__in=list_b)
            search = "Library: '" + library.name + "'"


        elif idG != 0:
            genre = Genre.objects.get(pk=idG)
            books = Books.objects.filter(genre=genre)
            search = "Genre: '" + genre.name + "'"


        elif idC != 0:
            collection = Collection.objects.get(id=idC)
            books = Books.objects.filter(collection=collection)
            search = "Collection: '" + collection.name + "'"

        else:
            books = Books.objects.all()
            search = "All books"
        
    return render(request, 'lib/book/list_books.html', {'books': books, 'search': search})

#admin
def details_book_admin(request, id):
    try:
        book = Books.objects.get(pk=id)
        instances = InstanceBook.objects.filter(id_books=id)

    except Books.DoesNotExist or InstanceBook.DoesNotExist:
        return redirect('list_books_admin')

    return render(request, "admin/book/details_book.html", {
        "book": book,
        "instances": instances
    })

def add_book_admin(request):

    if request.method == 'POST':
    
        data = Books()
        data.title = request.POST["title"]
        data.author = request.POST["author"]
        data.url_image = request.POST["url_image"]
        data.publisher = request.POST["publisher"]
        collec = Collection.objects.get(pk=request.POST["collection"])
        gen = Genre.objects.get(pk=request.POST["genre"])
        data.collection = collec
        data.genre = gen

        data.save()

        messages.success(request, 'Books added')

        return redirect('list_books_admin')

    else:
        return render(request, 'admin/book/add_book_admin.html')

def delete_book_admin(request,id):
    try:
        book = Books.objects.get(pk=id)
        book.delete()
        messages.success(request, 'book deleted')

    except Books.DoesNotExist:
        messages.error(request, 'error')

    return redirect('list_books_admin')

def list_books_admin(request):
    return render(request, 'admin/book/list_books.html')


##Instance
#site
def list_borrows(request):
    instances = InstanceBook.objects.filter(id_user=request.user)
    return render(request, 'lib/book/list_borrows.html', { 'instances': instances })

#admin
def add_instance_admin(request,id):
    book = Books.objects.get(pk=id)

    context_list = {
        'book': book
    }

    if request.method == 'POST':

        n = int(request.POST["nb"]);

        for nb in range(n):
                
            data = InstanceBook()
            # userr = User.objects.get(pk=request.user.id)
            # data.id_user = userr
            data.id_books = book
            lib_id = Library.objects.get(pk=request.POST["library"])
            data.id_library = lib_id

            data.save()

        if n > 1:
            messages.success(request, 'Instance added')
        else :
            messages.success(request, 'Instances added')

        return redirect('list_books_admin')
        

    else:
        return render(request, 'admin/book/add_instance_admin.html', context_list)

def delete_instance_admin(request,id):
    try:
        instance = InstanceBook.objects.get(pk=id)
        instance.delete()
        messages.success(request, 'instance deleted')

    except InstanceBook.DoesNotExist:
        messages.error(request, 'error')
        
    return redirect('list_books_admin')

def borrow_book_admin(request,id):
    try:
        instance = InstanceBook.objects.get(pk=id)

        if request.method == 'POST':
            

            user = User.objects.get(pk=request.POST["user"])
            instance.id_user = user
            instance.borrowing_date = datetime.datetime.now()
            instance.max_date = request.POST["max_date"]
            instance.status = 1
            instance.save()

            messages.success(request, 'Book borrowed')
            return redirect('list_books_admin')

        else :
            return render(request, 'admin/book/borrow_book_admin.html', { 'instance': instance})

    except InstanceBook.DoesNotExist:
        messages.error(request, 'error')
        return redirect('list_books_admin')

def cancel_borrow_admin(request,id):
    try:
        instance = InstanceBook.objects.get(pk=id)
        instance.id_user = None
        instance.borrowing_date = None
        instance.max_date = None
        instance.status = 0
        instance.save()

        messages.success(request, 'Borrow canceled')
        return redirect('list_books_admin')

    except InstanceBook.DoesNotExist:
        messages.error(request, 'error')
        return redirect('list_books_admin')

def list_borrows_admin(request):
    # instance = InstanceBook.objects.get(pk=2)
    # messages.success(request, instance.max_date)

    return render(request, 'admin/book/list_borrows.html')


##Library
#admin
def add_library_admin(request):

    if request.method == 'POST':
    
        library = Library()

        library.name = request.POST["name"]
        library.address_name = request.POST["address_name"]
        library.address_city = request.POST["address_city"]
        library.address_country = request.POST["address_country"]
        library.address_zip_code = request.POST["address_zip_code"]

        library.save()

        messages.success(request, 'Library added')
        return redirect('list_libraries_admin')

        

    else:
        return render(request, 'admin/library/add_library_admin.html')

def list_libraries_admin(request):
    return render(request, "admin/library/list_libraries_admin.html")

def edit_library_admin(request, id):
    try:
        library = Library.objects.get(pk=id)

        if request.method == 'POST':
            
            library.name = request.POST["name"]
            library.address_name = request.POST["address_name"]
            library.address_city = request.POST["address_city"]
            library.address_country = request.POST["address_country"]
            library.address_zip_code = request.POST["address_zip_code"]
            library.save()

            messages.success(request, "library modified")
            return redirect('list_libraries_admin')
            
        else :
            return render(request, "admin/library/edit_library_admin.html", { 'library': library })

    except Library.DoesNotExist:
        messages.error(request, 'error')
        return redirect('list_libraries_admin')

def delete_library_admin(request, id):
    try:
        lib = Library.objects.get(pk=id)
        lib.delete()
        messages.success(request, 'library deleted')
    except Library.DoesNotExist:
        messages.error(request, 'error')
    
    # return render(request, 'admin/library/list_libraries_admin.html')
    return redirect('list_libraries_admin')


##User
#admin
def list_users_admin(request):  
    return render(request, "admin/user/list_users_admin.html")

def edit_user_admin(request, id):
    try:
        user = User.objects.get(id=id)
        lib = Librarian.objects.get(id_user=id)
  
        if request.method == 'POST':
            
            user.username = request.POST["username"]
            user.email = request.POST["email"]
            user.save()

            idLib = Library.objects.get(pk=request.POST["library"])

            # if lib == None:
            #     lib = Librarian()
            #     lib.id_user = user

            lib.id_library = idLib
            lib.save()
            messages.success(request, "user modified")
            return redirect('list_users_admin')


        else :
            context = {
                        'user': user,
                        'lib': lib
                }

            return render(request, "admin/user/edit_user_admin.html", context)

    except Librarian.DoesNotExist:
        lib=None
        if request.method == 'POST':
            
            user.username = request.POST["username"]
            user.email = request.POST["email"]
            user.role = request.POST["role"]
            user.save()

            idLib = Library.objects.get(pk=request.POST["library"])


            lib = Librarian()
            lib.id_user = user

            lib.id_library = idLib
            lib.save()
            messages.success(request, "user modified")
            return redirect('list_users_admin')

        else :
            messages.warning(request, "No library attached, please select one or the first in the list will be assigned")
            context = {
                        'user': user,
                        'lib': lib
                }

            return render(request, "admin/user/edit_user_admin.html", context)

def delete_user_admin(request,id):
    try:
        user = User.objects.get(pk=id)
        user.delete()
        messages.success(request, 'user deleted')

    except User.DoesNotExist:
        messages.error(request, 'error')
        
    return render('list_users_admin')


##Lecture Group
#site
def details_lg(request,id):
    try:
        lecture_group = LectureGroup.objects.get(pk=id)
        lecturer = Lecturer.objects.filter(id_lg=lecture_group)
        lg_details = LectureGroupDetails.objects.filter(id_lg=lecture_group)

    except LectureGroup.DoesNotExist:
        return render('list_lecture_groups')

    return render(request, "lib/lecture_group/details_lecture_group.html", {
        "lecture_group": lecture_group,
        "lecturer": lecturer,
        "lg_details": lg_details,
    })
    
def list_lecture_group(request):
    return render(request, 'lib/lecture_group/list_lecture_group.html')

def list_lecture_groups(request):
    return render(request, "lib/lecture_group/list_lecture_groups.html")

def delete_lecturer(request,id):
    try:
        lect = Lecturer.objects.get(pk=id)
        lect.delete()
        messages.success(request, 'lecturer deleted')

    except Lecturer.DoesNotExist:
        messages.error(request, 'error')
        
    return redirect('list_lecture_group')

def add_lecture_group(request):
    
    if request.method == 'POST':
    
        lecture_group = LectureGroup()

        # lecture_group.date = request.POST["date"]
        lecture_group.title = request.POST["title"]
        lecture_group.address = request.POST["address"]

        # lg_details = LectureGroupDetails()

        # lg_details.id_lg = LectureGroup.objects.get(pk=lecture_group)

        lecture_group.save()

        messages.success(request, 'Lecture groupe added')
        return redirect('details_lg', id=lecture_group.pk)

    else:
        return render(request, 'lib/lecture_group/add_lecture_group_admin.html')

def add_lecture_group_details(request, id):
    try:
        lg = LectureGroup.objects.get(pk=id)

        if request.method == 'POST':

            lg_details = LectureGroupDetails()

            if request.POST["date_start"] > request.POST["date_end"]:
                messages.error(request, 'Date satrt > date end')
                return redirect('details_lg', id=id)

            lg_details.date_start = request.POST["date_start"]
            lg_details.date_end = request.POST["date_end"]
            lg_details.id_lg = lg

            lg_details.save()

            messages.success(request, 'Lecture groupe details added')
            return redirect('details_lg', id=id)

        else:
            return render(request, 'lib/lecture_group/add_lecture_details.html', { 'lg':lg })
    
    except LectureGroup.DoesNotExist:
        messages.error(request, "Error")
        return redirect('list_lecture_group')

def add_lecturer(request, id):
    try :
        lg = LectureGroup.objects.get(pk=id)
        lect = Lecturer.objects.filter(id_lg=lg)
        usr = User.objects.exclude(id__in=lect)

        if request.method == 'POST':
            
            lect = Lecturer()
            lect.id_user = User.objects.get(pk=request.user.id)
            lect.id_lg = lg
            lect.save()

            #TODO envoyer un mail

            messages.success(request, 'Lecturer added')
            return redirect('details_lg', id=id)

    except LectureGroup.DoesNotExist or User.DoesNotExist:
        messages.error(request, "Error")
        return redirect('list_lecture_group')

#admin
def list_lecture_group_admin(request):
    return render(request, 'admin/lecture_group/list_lecture_group.html')

def add_lecture_group_admin(request):
    
    if request.method == 'POST':
    
        lecture_group = LectureGroup()

        lecture_group.date = request.POST["date"]
        lecture_group.title = request.POST["title"]
        lecture_group.address = request.POST["address"]

        lecture_group.save()

        messages.success(request, 'Lecture groupe added')
        return redirect('list_lecture_group_admin')

    else:
        return render(request, 'admin/lecture_group/add_lecture_group_admin.html')

def edit_lecture_group_admin(request, id):
    try:
        lecture_group = LectureGroup.objects.get(pk=id)
  
        if request.method == 'POST':
            
            lecture_group.date = request.POST["date"]
            lecture_group.title = request.POST["title"]
            lecture_group.address = request.POST["address"]
            lecture_group.save()
            messages.success(request, "lecture group modified")
            return redirect('list_lecture_group_admin')

        else :
            context = {
                        'lg': lecture_group
                }
            return render(request, "admin/lecture_group/edit_lecture_group_admin.html", context)

    except LectureGroup.DoesNotExist:
        return redirect('list_lecture_group_admin')

def delete_lecture_group_admin(request,id):
    try:
        lecture_group = LectureGroup.objects.get(pk=id)
        lecture_group.delete()
        messages.success(request, 'lecture group deleted')

    except User.DoesNotExist:
        messages.error(request, 'error')
        
    return redirect('list_lecture_group_admin')

def add_lecturer_admin(request, id):
    try :
        lg = LectureGroup.objects.get(pk=id)
        lect = Lecturer.objects.filter(id_lg=lg)
        usr = User.objects.exclude(id__in=list(lect.values_list("id", flat=True)))

        if request.method == 'POST':
    
            lect = Lecturer()
            lect.id_user = User.objects.get(pk=request.POST["user"])
            lect.id_lg = lg
            lect.save()

            messages.success(request, 'Lecturer added')
            return redirect('list_lecture_group_admin')

        else:
            return render(request, 'admin/lecture_group/add_lecturer.html', { 
                'lg':lg,
                'lect': lect,
                'usr': usr })

    except LectureGroup.DoesNotExist or User.DoesNotExist:
        messages.error(request, "Error")
        return redirect('list_lecture_group_admin')

def delete_lecturer_admin(request,id):
    try:
        lect = Lecturer.objects.get(pk=id)
        lect.delete()
        messages.success(request, 'lecturer deleted')

    except Lecturer.DoesNotExist:
        messages.error(request, 'error')
        
    return redirect('list_lecture_group_admin')

def details_lg_admin(request, id):
    try:
        lg = LectureGroup.objects.get(pk=id)
        lect = Lecturer.objects.filter(id_lg=id)

    except LectureGroup.DoesNotExist or Lecturer.DoesNotExist:
        return redirect('list_lecture_group_admin')

    return render(request, "admin/lecture_group/details_lg.html", {
        "lg": lg,
        "lect": lect
    })

def add_lecture_group_details_admin(request, id):
    try:
        lg = LectureGroup.objects.get(pk=id)

        if request.method == 'POST':

            lg_details = LectureGroupDetails()

            if request.POST["date_start"] > request.POST["date_end"]:
                messages.error(request, 'Date satrt > date end')
                return redirect('details_lg', id=id)

            lg_details.date_start = request.POST["date_start"]
            lg_details.date_end = request.POST["date_end"]
            lg_details.id_lg = lg

            lg_details.save()

            messages.success(request, 'Lecture groupe details added')
            return redirect('details_lg', id=id)

        else:
            return render(request, 'admin/lecture_group/add_lecture_details.html', { 'lg':lg })
    
    except LectureGroup.DoesNotExist:
        messages.error(request, "Error")
        return redirect('list_lecture_group_admin')


