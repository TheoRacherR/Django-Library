from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('404/', views.not_founded, name='not_founded'),
    path('signin/', views.signin_def, name='signin_def'),
    path('login/', views.login_def, name='login_def'),
    path('logout/', views.logout_def, name='logout_def'),

    path('book_page/<int:id>/', views.details_book, name='book_page'),
    path('add_book/', views.add_book, name='add_book'),
    path('list_books/', views.list_books, name='list_books'),
    path('add_instance/<int:id>/', views.add_instance, name='add_instance'),

    path('add_library/', views.add_library, name='add_library'),
    path('list_libraries/', views.list_libraries, name='list_libraries'),
    path('edit_library/<int:id>/', views.edit_library, name='edit_library'),

    path('list_peoples/', views.list_peoples, name='list_peoples'),
    path('edit_people/<int:id>/', views.edit_people, name='edit_people'),

]