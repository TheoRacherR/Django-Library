from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.template import Context, RequestContext
from django.db import IntegrityError

from .models import UserData, Message, Books, Genre, Collection, InstanceBook, Library, Librarian, LectureGroup, Lecturer, LectureGroupDetails, Forum
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

from rolepermissions.roles import assign_role, remove_role

import datetime

import folium
import geocoder



#site
def index(request):
    return render(request, "lib/index.html")

def not_founded(request):
    return render(request, 'lib/404.html')

def search(request):
    try:
        if request.method == 'POST':
            search = request.POST['search']
            location = geocoder.osm(search)
            lat = location.lat
            lng = location.lng
            m = folium.Map(location=[lat, lng], zoom_start=12)
            folium.Marker(location=[lat, lng], popup=search, icon=folium.Icon("red"), tooltip="Click here").add_to(m)

            librarys = Library.objects.all()
            for lib in librarys:
                address = lib.address_name + ', ' + lib.address_zip_code + ' ' + lib.address_city
                location = geocoder.osm(address)
                lat = location.lat
                lng = location.lng
                folium.Marker(location=[lat, lng], popup= lib.name + ' ' + address, tooltip="Click here").add_to(m)
                # folium.map.Popup(html="<div>" + address + "</div>")

            m = m._repr_html_()
            return render(request, "lib/search.html", { 'm': m })
        
        else:
            return redirect('index')

    except Library.DoesNotExist:
        messages.error(request, "Erro")
        return redirect("index")


#admin
def admin(request):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
        messages.error(request, '403, Access denied')
        return redirect('index')
    return render(request, 'admin/index.html')


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
                first_name=request.POST['firstname'],
                last_name=request.POST['lastname'],
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

#admin
def set_role(request,id,role):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin']:
            messages.error(request, '403, Access denied')
            return redirect('index')

        user = User.objects.get(pk=id)
        assign_role(user, role)
        if role != 'admin':
            remove_role(user, 'admin')
        if role != 'customer':
            remove_role(user, 'customer')
        if role != 'bookseller':
            remove_role(user, 'bookseller')
        usr = UserData.objects.get(user=user)
    except UserData.DoesNotExist:
        usr = UserData()
        usr.user = user

    usr.role = role
    usr.save()
    messages.success(request, 'Update user {user.username} with {role} role')
    return redirect('list_users_admin')



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

    m = ''
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
            location = geocoder.osm(library.address_name + ', ' + library.address_zip_code + ' ' + library.address_city)
            lat = location.lat
            lng = location.lng
            m = folium.Map(location=[lat, lng], zoom_start=12)
            folium.Marker([lat, lng]).add_to(m)
            m = m._repr_html_()


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
        
    return render(request, 'lib/book/list_books.html', {'books': books, 'search': search, 'm': m })

#admin
def details_book_admin(request, id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')

        book = Books.objects.get(pk=id)
        instances = InstanceBook.objects.filter(id_books=id)

    except Books.DoesNotExist or InstanceBook.DoesNotExist:
        return redirect('list_books_admin')

    return render(request, "admin/book/details_book.html", {
        "book": book,
        "instances": instances
    })

def add_book_admin(request):

    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')

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

        return redirect('book_page_admin', id=data.id)

    else:
        return render(request, 'admin/book/add_book.html')

def edit_book_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        book = Books.objects.get(pk=id)

        if request.method == 'POST':
        
            book.title = request.POST["title"]
            book.author = request.POST["author"]
            book.url_image = request.POST["url_image"]
            book.publisher = request.POST["publisher"]
            collec = Collection.objects.get(pk=request.POST["collection"])
            gen = Genre.objects.get(pk=request.POST["genre"])
            book.collection = collec
            book.genre = gen

            book.save()

            messages.success(request, 'Books edited')

            return redirect('book_page_admin', id=id)
        else :
            return render(request, "admin/book/edit_book.html", { 'book': book })

    except Books.DoesNotExist:
        messages.error(request, 'error')
        return redirect('list_books_admin')

def list_books_admin(request):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
        messages.error(request, '403, Access denied')
        return redirect('index')
    return render(request, 'admin/book/list_books.html')

def delete_book_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        book = Books.objects.get(pk=id)
        book.delete()
        messages.success(request, 'book deleted')

    except Books.DoesNotExist:
        messages.error(request, 'error')

    return redirect('list_books_admin')



##Collection
#admin
def list_collection_admin(request):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
        messages.error(request, '403, Access denied')
        return redirect('index')
    return render(request, 'admin/collection/list_collection.html')

def add_collection_admin(request):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
        messages.error(request, '403, Access denied')
        return redirect('index')
    if request.method == 'POST':
        coll = Collection()
        coll.name = request.POST['name']

        coll.save()
        return redirect('list_collection_admin')

    else:
        return render(request, 'admin/collection/add_collection.html')

def edit_collection_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        coll = Collection.objects.get(id=id)
        if request.method == 'POST':
            coll.name = request.POST['name']
            coll.save()

            messages.success(request, 'Collection edited')
            return redirect('list_collection_admin')
        else:
            return render(request, 'admin/collection/edit_collection.html', { 'coll': coll })

    except Collection.DoesNotExist:
        messages.error(request, "Error")
        return redirect('list_collection_admin')

def delete_collection_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        coll = Collection.objects.get(id=id)
        Books.objects.filter(collection=coll).update(collection = Collection.objects.get(name='No collection'))
        coll.delete()
        messages.success(request, 'Collection deleted')

    except Collection.DoesNotExist:
        messages.error(request, "Error")
    
    return redirect('list_collection_admin')



##Genre
#admin
def list_genre_admin(request):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
        messages.error(request, '403, Access denied')
        return redirect('index')
    return render(request, 'admin/genre/list_genre.html')

def add_genre_admin(request):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
        messages.error(request, '403, Access denied')
        return redirect('index')
    if request.method == 'POST':
        gen = Genre()
        gen.name = request.POST['name']

        gen.save()
        return redirect('list_genre_admin')

    else:
        return render(request, 'admin/genre/add_genre.html')

def edit_genre_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        gen = Genre.objects.get(id=id)
        if request.method == 'POST':
            gen.name = request.POST['name']
            gen.save()

            messages.success(request, 'Genre edited')
            return redirect('list_genre_admin')
        else:
            return render(request, 'admin/genre/edit_genre.html', { 'gen':gen })

    except Genre.DoesNotExist:
        messages.error(request, "Error")
        return redirect('list_genre_admin')

def delete_genre_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        gen = Genre.objects.get(id=id)
        Books.objects.filter(genre=gen).update(genre = Genre.objects.get(name='No genre'))
        gen.delete()
        messages.success(request, 'Genre deleted')

    except Genre.DoesNotExist:
        messages.error(request, "Error")
    
    return redirect('list_genre_admin')



##Instance
#site
def list_borrows(request):
    if request.user.is_authenticated:
        instances = InstanceBook.objects.filter(id_user=request.user)
        return render(request, 'lib/book/list_borrows.html', { 'instances': instances })
    else:
        messages.error(request, "403, You are not connected")
        return redirect("login_def")
    

#admin
def add_instance_admin(request,id):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
        messages.error(request, '403, Access denied')
        return redirect('index')
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
        return render(request, 'admin/book/add_instance.html', context_list)

def delete_instance_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        instance = InstanceBook.objects.get(pk=id)
        instance.delete()
        messages.success(request, 'instance deleted')

    except InstanceBook.DoesNotExist:
        messages.error(request, 'error')
        
    return redirect('list_books_admin')

def borrow_book_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')
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
            return render(request, 'admin/book/borrow_book.html', { 'instance': instance})

    except InstanceBook.DoesNotExist:
        messages.error(request, 'error')
        return redirect('list_books_admin')

def cancel_borrow_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')
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
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
        messages.error(request, '403, Access denied')
        return redirect('index')

    return render(request, 'admin/book/list_borrows.html')



##Library
#admin
def add_library_admin(request):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin']:
        messages.error(request, '403, Access denied')
        return redirect('index')

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
        return render(request, 'admin/library/add_library.html')

def list_libraries_admin(request):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
        messages.error(request, '403, Access denied')
        return redirect('index')
    else :
        return render(request, "admin/library/list_libraries.html")

def edit_library_admin(request, id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')
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
            return render(request, "admin/library/edit_library.html", { 'library': library })

    except Library.DoesNotExist:
        messages.error(request, 'error')
        return redirect('list_libraries_admin')

def delete_library_admin(request, id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        lib = Library.objects.get(pk=id)
        lib.delete()
        messages.success(request, 'library deleted')
    except Library.DoesNotExist:
        messages.error(request, 'error')
    
    # return render(request, 'admin/library/list_libraries.html')
    return redirect('list_libraries_admin')

def library_page_admin(request, id):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
        messages.error(request, '403, Access denied')
        return redirect('index')
    lib = Library.objects.get(pk=id)
    return render(request, "admin/library/library_page.html", { 'lib': lib })



##User
#site

def user_page(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Your are not connected')
        return redirect('login_def')
    
    user = request.user
    user_data = UserData.objects.get(user=user)
    librarian = Librarian.objects.filter(id_user=user)
    instance = InstanceBook.objects.filter(id_user=user)
    lecture_group = LectureGroup.objects.filter(owner=user)
    lecturer = Lecturer.objects.filter(id_user=user)
    message = Message.objects.filter(id_user=user)

    context = {
        'user': user,
        'user_data': user_data,
        'librarian': librarian,
        'instance': instance,
        'lecture_group': lecture_group,
        'lecturer': lecturer,
        'message': message,
    }
    return render(request, 'lib/user/user_page.html', context)

def edit_user(request):
    try:
        if not request.user.is_authenticated:
            messages.error(request, 'Your are not connected')
            return redirect('login_def')

        user = request.user
  
        if request.method == 'POST':
            
            user.username = request.POST["username"]
            user.email = request.POST["email"]
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.save()

            messages.success(request, "user modified")
            return redirect('user_page')


        else:
            return render(request, "lib/user/edit_user.html", { "user": user })

    except User.DoesNotExist:
        return redirect("index")

#admin
def page_user(request, id):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
        messages.error(request, '403, Access denied')
        return redirect('index')
    user = User.objects.get(pk=id)
    user_data = UserData.objects.get(user=user)
    librarian = Librarian.objects.filter(id_user=user)
    instance = InstanceBook.objects.filter(id_user=user)
    lecture_group = LectureGroup.objects.filter(owner=user)
    lecturer = Lecturer.objects.filter(id_user=user)
    message = Message.objects.filter(id_user=user)

    context = {
        'user': user,
        'user_data': user_data,
        'librarian': librarian,
        'instance': instance,
        'lecture_group': lecture_group,
        'lecturer': lecturer,
        'message': message,
    }
    return render(request, 'admin/user/page_user.html', context)

def list_users_admin(request):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
        messages.error(request, '403, Access denied')
        return redirect('index')
    return render(request, "admin/user/list_users.html")

def edit_user_admin(request, id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin']:
            messages.error(request, '403, Access denied')
            return redirect('index')
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

            return render(request, "admin/user/edit_user.html", context)

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

            return render(request, "admin/user/edit_user.html", context)

def delete_user_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        user = User.objects.get(pk=id)
        user.delete()
        messages.success(request, 'user deleted')

    except User.DoesNotExist:
        messages.error(request, 'error')
        
    return redirect('list_users_admin')



##Book Group
#site
def lg_page(request,id):
    try:
        lecture_group = LectureGroup.objects.get(pk=id)

        lecturer = Lecturer.objects.filter(id_lg=lecture_group)
        lg_details = LectureGroupDetails.objects.filter(id_lg=lecture_group)

        location = geocoder.osm(lecture_group.address + " France")
        lat = location.lat
        lng = location.lng
        m = folium.Map(location=[lat, lng], zoom_start=12)
        folium.Marker(location=[lat, lng], popup=lecture_group.address, icon=folium.Icon("green"), tooltip="Click here").add_to(m)
        m = m._repr_html_()

    except LectureGroup.DoesNotExist:
        return render('list_lecture_groups')

    return render(request, "lib/book_group/details_lecture_group.html", {
        "lecture_group": lecture_group,
        "lecturer": lecturer,
        "lg_details": lg_details,
        "m": m
    })

def list_lecture_groups(request):
    if request.user.is_authenticated:
        return render(request, "lib/book_group/list_lecture_groups.html")
    else:
        messages.error(request, "403, You are not connected")
        return redirect("login_def")

def add_lecture_group(request):
    
    if request.method == 'POST':
    
        lecture_group = LectureGroup()
        
        lecture_group.owner = User.objects.get(pk=request.user.id)
        lecture_group.title = request.POST["title"]
        lecture_group.address = request.POST["address"]

        lecture_group.save()

        messages.success(request, 'Book group added')
        return redirect('lg_page', id=lecture_group.pk)

    else:
        return render(request, 'lib/book_group/add_lecture_group.html')

def delete_lecture_group(request,id):
    try:
        lecture_group = LectureGroup.objects.get(pk=id)
        lecture_group.delete()
        messages.success(request, 'book group deleted')

    except LectureGroup.DoesNotExist:
        messages.error(request, 'error')
        
    return redirect('list_lecture_groups')

def add_lecture_group_details(request, id):
    try:
        lg = LectureGroup.objects.get(pk=id)
        lg_details = LectureGroupDetails()

        if request.POST["date_start"] > request.POST["date_end"]:
            messages.error(request, 'Date start > date end')
            return redirect('lg_page', id=id)

        lg_details.date_start = request.POST["date_start"]
        lg_details.date_end = request.POST["date_end"]
        lg_details.id_lg = lg

        lg_details.save()

        messages.success(request, 'Book group details added')
    
    except LectureGroup.DoesNotExist:
        messages.error(request, "Error")
        return redirect('list_lecture_group')

    return redirect('lg_page', id=id)
    
def delete_lecture_group_details(request, id):
    try:
        lg = LectureGroupDetails.objects.get(pk=id)
        idLG = lg.id_lg.id

        lg.delete()
        messages.success(request, "Session deleted")
        
    except LectureGroupDetails.DoesNotExist:
        messages.error(request, "Error")
    
    return redirect('lg_page', id=idLG)

def add_lecturer(request, id):
    try :
        lg = LectureGroup.objects.get(pk=id)
        lect = Lecturer.objects.filter(id_lg=lg)
        usr = User.objects.exclude(id__in=lect)

        if request.method == 'POST':
            
            lect = Lecturer()
            lect.id_user = User.objects.get(pk=request.POST['user'])
            lect.id_lg = lg
            lect.save()

            #TODO envoyer un mail

            messages.success(request, 'Lecturer added')

    except User.DoesNotExist:
        messages.error(request, "Error")
    
    return redirect('lg_page', id=id)

def delete_lecturer(request,id):
    try:
        lect = Lecturer.objects.get(pk=id)
        idLG = lect.id_lg.id
        lect.delete()
        messages.success(request, 'lecturer deleted')

    except Lecturer.DoesNotExist:
        messages.error(request, 'error')
        
    return redirect('lg_page', id=idLG)

#admin
def list_lecture_group_admin(request):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
        messages.error(request, '403, Access denied')
        return redirect('index')
    return render(request, 'admin/book_group/list_lecture_group.html')

def add_lecture_group_admin(request):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin']:
        messages.error(request, '403, Access denied')
        return redirect('index')
    
    if request.method == 'POST':
    
        lecture_group = LectureGroup()

        lecture_group.title = request.POST["title"]
        lecture_group.address = request.POST["address"]

        lecture_group.save()

        messages.success(request, 'book groupe added')
        return redirect('list_lecture_group_admin')

    else:
        return render(request, 'admin/book_group/add_lecture_group.html')

def edit_lecture_group_admin(request, id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        lecture_group = LectureGroup.objects.get(pk=id)
  
        if request.method == 'POST':
            
            lecture_group.title = request.POST["title"]
            lecture_group.address = request.POST["address"]
            lecture_group.save()
            messages.success(request, "book group modified")
            return redirect('list_lecture_group_admin')

        else :
            context = {
                        'lg': lecture_group
                }
            return render(request, "admin/book_group/edit_lecture_group.html", context)

    except LectureGroup.DoesNotExist:
        return redirect('list_lecture_group_admin')

def delete_lecture_group_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        lecture_group = LectureGroup.objects.get(pk=id)
        lecture_group.delete()
        messages.success(request, 'book group deleted')

    except User.DoesNotExist:
        messages.error(request, 'error')
        
    return redirect('list_lecture_group_admin')

def add_lecturer_admin(request, id):
    try :
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        lg = LectureGroup.objects.get(pk=id)
        lect = Lecturer.objects.filter(id_lg=lg)
        usr = User.objects.exclude(id__in=list(lect.values_list("id", flat=True)))

        if request.method == 'POST':
    
            lect = Lecturer()
            lect.id_user = User.objects.get(pk=request.POST["user"])
            lect.id_lg = lg
            lect.save()

            messages.success(request, 'Lecturer added')
            return redirect('details_lg_admin', id=id)

        else:
            return render(request, 'admin/book_group/add_lecturer.html', { 
                'lg':lg,
                'lect': lect,
                'usr': usr })

    except LectureGroup.DoesNotExist or User.DoesNotExist:
        messages.error(request, "Error")
        return redirect('list_lecture_group_admin')

def delete_lecturer_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        lect = Lecturer.objects.get(pk=id)
        idLG = lect.id_lg.id
        lect.delete()
        messages.success(request, 'lecturer deleted')

    except Lecturer.DoesNotExist:
        messages.error(request, 'error')
        
    return redirect('details_lg_admin', id=idLG)

def details_lg_admin(request, id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        lg = LectureGroup.objects.get(pk=id)
        lect = Lecturer.objects.filter(id_lg=id)

    except LectureGroup.DoesNotExist or Lecturer.DoesNotExist:
        return redirect('list_lecture_group_admin')

    return render(request, "admin/book_group/lg_page.html", {
        "lg": lg,
        "lect": lect
    })

def add_lecture_group_details_admin(request, id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        lg = LectureGroup.objects.get(pk=id)

        if request.method == 'POST':

            lg_details = LectureGroupDetails()

            if request.POST["date_start"] > request.POST["date_end"]:
                messages.error(request, 'Date satrt > date end')
                return redirect('lg_page', id=id)

            lg_details.date_start = request.POST["date_start"]
            lg_details.date_end = request.POST["date_end"]
            lg_details.id_lg = lg

            lg_details.save()

            messages.success(request, 'book groupe details added')
            return redirect('lg_page', id=id)

        else:
            return render(request, 'admin/book_group/add_lecture_details.html', { 'lg':lg })
    
    except LectureGroup.DoesNotExist:
        messages.error(request, "Error")
        return redirect('list_lecture_group_admin')



##Forum
#site
def list_forum(request):
    return render(request, 'lib/forum/list_forum.html')

def add_forum(request):
    forum = Forum()

    if request.method == 'POST':
        forum.title = request.POST['title']
        forum.save()
        messages.success(request, 'forum added')
        return redirect('list_forum')
    
    else:
        return render(request, 'lib/forum/add_forum.html')

def delete_forum(request,id):
    try:
        forum = Forum.objects.get(pk=id)
        forum.delete()

        messages.success(request, 'Forum deleted')
        return redirect('list_forum')

    except Forum.DoesNotExist:
        messages.error(request, 'error')
        return redirect('list_forum')

def forum_page(request,id):
    try:
        forum = Forum.objects.get(pk=id)
        message = Message.objects.filter(id_forum=forum).order_by('-creation_date')

        return render(request, 'lib/forum/forum_page.html', {
            'forum': forum,
            'messages': message,
        })

    except Forum.DoesNotExist:
        messages.error(request, 'error')
        return redirect('list_forum')

def list_own_message(request):
    try:
        message = Message.objects.filter(id_user=request.user)
        return render(request, 'lib/forum/list_message.html', { 'message': message })

    except Message.DoesNotExist:
        messages.error(request, "Error")
        return redirect('admin')
        
def add_message(request,id):
    message = Message()

    if request.method == 'POST':
        message.text = request.POST['text']
        message.id_forum = Forum.objects.get(pk=id)
        message.id_user = User.objects.get(id=request.user.id)
        message.save()
        messages.success(request, 'message added')
        return redirect('forum_page', id=id)
    
    else:
        return redirect('forum_page', id=id)

def edit_message(request,id):
    try:
        message = Message.objects.get(id=id)
        if request.method == 'POST':
            message.text = request.POST['text']
            message.save()
            messages.success(request, 'message edited')
            return redirect('forum_page', id=message.id_forum.pk)
        else:
            return render(request, "lib/forum/edit_message.html", { "message": message })

    except Message.DoesNotExist:
        messages.error(request, 'errors')
        return redirect('list_forum')

def delete_message(request,id):
    try:
        if request.user != Message.objects.get(id=id).id_user:
            messages.error(request, '403, You are not the owner of this message')
            return redirect('index')
        message = Message.objects.get(id=id)
        message.delete()
        messages.success(request, 'message deleted')
        return redirect('list_message')

    except Message.DoesNotExist:
        messages.error(request, 'error')

##admin
def list_forums_admin(request):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
        messages.error(request, '403, Access denied')
        return redirect('index')
    return render(request, 'admin/forum/list_forum.html')

def add_forum_admin(request):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
        messages.error(request, '403, Access denied')
        return redirect('index')
    forum = Forum()
    if request.method == 'POST':
        forum.title = request.POST['title']
        forum.text = request.POST['text']
        forum.save()
        messages.success(request, 'Forum added')
        return redirect('list_forums_admin')
    
    else:
        return render(request, 'admin/forum/add_forum.html')

def edit_forum_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')

        forum = Forum.objects.get(id=id)
        if request.method == 'POST':
            forum.title = request.POST['title']
            forum.title = request.POST['title']
            forum.save()
            messages.success(request, 'Forum edited')
            return redirect('list_forums_admin')
        
        else:
            return render(request, 'admin/forum/edit_forum.html')
    except Forum.DoesNotExist:
        messages.error(request, "error")
        return render('list_forums_admin')   

def delete_forum_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        forum = Forum.objects.get(pk=id)
        forum.delete()

        messages.success(request, 'Forum deleted')
        return redirect('list_forums_admin')

    except Forum.DoesNotExist:
        messages.error(request, 'error')
        return redirect('list_forums_admin')

def forum_page_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        forum = Forum.objects.get(pk=id)
        messages = Message.objects.filter(id_forum=forum).order_by('-creation_date')

        return render(request, 'admin/forum/forum_page.html', {
            'forum': forum,
            'messages': messages,
        })

    except Forum.DoesNotExist:
        messages.error(request, 'error')
        return redirect('list_forums_admin')

def edit_message_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        if request.method == 'POST':
            message = Message.objects.get(pk=id)
            message.id_user = User.objects.get(id=request.POST['user'])
            message.id_forum = Forum.objects.get(id=request.POST['forum'])
            message.text = request.POST['text']
            message.save()
            messages.success(request, "Message edited")
            return redirect("list_message_admin")
        else:
            return render(request, "admin/forum/edit_message.html")

    except Message.DoesNotExist:
        messages.error(request, "Error")
        return render("list_message_admin")

def delete_message_admin(request,id):
    try:
        if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
            messages.error(request, '403, Access denied')
            return redirect('index')
        message = Message.objects.get(pk=id)
        message.delete()
        messages.success(request, "Message deleted")
        return render("list_message_admin")

    except Message.DoesNotExist:
        messages.error(request, "Error")
        return render("list_message_admin")

def list_message_admin(request):
    if request.user.is_authenticated and UserData.objects.get(user=request.user).role not in ['admin', 'bookseller']:
        messages.error(request, '403, Access denied')
        return redirect('index')
    return render(request, "admin/forum/list_message.html")


#Librarian
#admin

# def list_librarians_admin

#def add_librarian_admin

def delete_librarian_admin(request,id):
    try:
        message = Librarian.objects.get(pk=id)
        message.delete()
        messages.success(request, "Librarian deleted")
        return render(request, "admin/forum/list_message.html")

    except Librarian.DoesNotExist:
        messages.error(request, "Error")
        return redirect("index")

