from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.template import Context, RequestContext
from django.db import IntegrityError

from .models import People, Books, Genre, Collection, InstanceBooks, Library, Librarian
from .forms import AddBookForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User



def index(request):
    return render(request, "lib/index.html")

def not_founded(request):
    return redirect('/lib/404') 

def details_book(request, id):
    try:
        book = Books.objects.get(pk=id)
        instances = InstanceBooks.objects.filter(id_books=id)

    except Books.DoesNotExist or InstanceBooks.DoesNotExist:
        return render(request, 'lib/404.html')

    return render(request, "lib/book/details_book.html", {
        "book": book,
        "instances": instances
    })

def list_books(request):
    try:
        books = Books.objects.all()
    except Books.DoesNotExist:
        raise Http404("List Books does not exist")  
    return render(request, "lib/book/list_books.html", context={"books": books})

def add_book(request):
    collection = Collection.objects.all()
    genre = Genre.objects.all()
    context_list = {
        'collection' : collection,
        'genre' : genre
    }

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
        books = Books.objects.all()

        return render(request, "lib/book/list_books.html", context={"books": books})
        

    else:
        return render(request, 'lib/book/add_book.html', context_list)

def add_instance(request,id):
    library = Library.objects.all()
    book = Books.objects.get(pk=id)

    context_list = {
        'library': library,
        'book': book
    }

    if request.method == 'POST':
    
        data = InstanceBooks()
        userr = People.objects.get(pk=request.user.pk)
        data.id_user = userr
        data.id_books = book
        lib_id = Library.objects.get(pk=request.POST["library"])
        data.id_library = lib_id

        data.save()

        messages.success(request, 'Instance added')

        return redirect("/lib/list_books")
        

    else:
        return render(request, 'lib/book/add_instance.html', context_list)

def login_def(request):
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
        if request.method == 'POST':
            
            people = People()
            people.username = request.POST['username']
            people.email = request.POST['email']
            people.password = make_password(request.POST['password'])
            people.save()

            user_admin = User.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=make_password(request.POST['password'])
            )
            user_admin.save() #ne marche pas

            people_verif = People.objects.get(username=people.username, email=people.email, password=people.password)

            librarian = Librarian()
            librarian.id_user = people

            lib = Library.objects.get(pk=4)

            librarian.id_library = lib

            librarian.save()


            if people_verif:
                # user_auth = authenticate(request, username=request.POST['username'], password=request.POST['password'])

            #     if user_auth is not None:
            #         login(request, people)
            #         return redirect('/lib/')
            #     else:
                messages.success(request, 'User created')
                return redirect('/lib/')
            else:
                messages.error(request, 'Erro happened')
                return redirect('/lib/signin/')

        else:
            return render(request, 'lib/auth/signin.html')
    except IntegrityError:
        messages.error(request, 'This username already exist')
        return render(request, 'lib/auth/signin.html')

def logout_def(request):
    logout(request)
    return redirect('/lib/signin')

def add_library(request):

    if request.method == 'POST':
    
        library = Library()

        library.name = request.POST["name"]
        library.address_name = request.POST["address_name"]
        library.address_city = request.POST["address_city"]
        library.address_country = request.POST["address_country"]
        library.address_zip_code = request.POST["address_zip_code"]

        library.save()

        messages.success(request, 'Library added')
        libraries = Library.objects.all()

        return render(request, "lib/library/list_libraries.html", context={"libraries": libraries})
        

    else:
        return render(request, 'lib/library/add_library.html')

def list_libraries(request):
    try:
        libraries = Library.objects.all()
    except Library.DoesNotExist:
        raise Http404("List Library does not exist")  
    return render(request, "lib/library/list_libraries.html", context={"libraries": libraries})

def edit_library(request, id):
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
            return redirect('/lib/list_libraries')
            
        else :
            return render(request, "lib/library/edit_library.html", { 'library': library})

    except Library.DoesNotExist:
        return render(request, 'lib/404.html')

def list_peoples(request):
    try:
        peoples = People.objects.all().order_by('-creation_date')
    except Library.DoesNotExist:
        raise Http404("List Library does not exist")  
    return render(request, "lib/people/list_peoples.html", context={"peoples": peoples})

def edit_people(request, id):
    try:
        people = People.objects.get(pk=id)
        library = Library.objects.all()
        lib = Librarian.objects.get(id_user=id)

        if request.method == 'POST':
            
            people.username = request.POST["username"]
            people.email = request.POST["email"]
            people.role = request.POST["role"]
            people.save()

            idLib = Library.objects.get(pk=request.POST["library"])
            lib.id_library = idLib
            lib.save()

            messages.success(request, "people modified")
            return redirect('/lib/list_peoples')

        else :
            context = {
                        'people': people,
                        'library': library,
                        'lib': lib
                }

            return render(request, "lib/people/edit_people.html", context)
            
    except Librarian.DoesNotExist:
        lib=None
        messages.warning(request, "No library attached, please select one or the first in the list will be assigned")

    

