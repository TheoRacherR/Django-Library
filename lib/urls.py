from django.urls import path
from django.contrib.auth.decorators import permission_required

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('404/', views.not_founded, name='not_founded'),
    path('signin/', views.signin_def, name='signin_def'),
    path('login/', views.login_def, name='login_def'),
    path('logout/', views.logout_def, name='logout_def'),

    path('book/page/<int:id>/', views.details_book, name='book_page'),
    path('book/list/lib=<int:idL>&col=<int:idC>&gen=<int:idG>', views.list_books, name='list_books'),
    #user account
    path('bookgroup/add', views.add_lecture_group, name='add_lecture_group'),
    path('bookgroup/detail/<int:id>', views.details_lg, name='details_lg'),
    path('bookgroup/mylist/', views.list_lecture_group, name='list_lecture_group'),
    path('bookgroup/list/', views.list_lecture_groups, name='list_lecture_groups'),
    path('bookgroup/people/add/<int:id>', views.add_lecturer, name='add_lecturer'),
    path('bookgroup/people/delete/<int:id>', views.delete_lecturer, name='delete_lecturer'),
    path('bookgroup/session/add/<int:id>', views.add_lecture_group_details, name='add_lecture_group_details'),
    
    path('borrow/list/', views.list_borrows, name='list_book_borrowed'),


    ##Admin
    path('admin/', views.admin, name='admin'),

    path('admin/instance/add/<int:id>/', views.add_instance_admin, name='add_instance_admin'),
    path('admin/instance/delete/<int:id>/', views.delete_instance_admin, name='delete_instance_admin'),

    path('admin/book/add/', views.add_book_admin, name='add_book_admin'),
    path('admin/book/delete/<int:id>/', views.delete_book_admin, name='delete_book_admin'),
    path('admin/book/list/', views.list_books_admin, name='list_books_admin'),
    path('admin/book/page/<int:id>/', views.details_book_admin, name='book_page_admin'),
    #edit book

    path('admin/library/add/', views.add_library_admin, name='add_library_admin'),
    path('admin/library/delete/<int:id>', views.delete_library_admin, name='delete_library_admin'),
    path('admin/library/edit/<int:id>/', views.edit_library_admin, name='edit_library_admin'),
    path('admin/library/list/', views.list_libraries_admin, name='list_libraries_admin'),
    path('admin/library/borrows/<int:id>', views.borrow_book_admin, name='borrow_book_admin'),
    path('admin/library/borrows/cancel/<int:id>', views.cancel_borrow_admin, name='cancel_borrow_admin'),
    path('admin/library/borrows/list/', views.list_borrows_admin, name='list_borrows_admin'),
    # path('admin/library/page/', views., name=''),

    path('admin/users/list/', views.list_users_admin, name='list_users_admin'),
    path('admin/users/edit/<int:id>/', views.edit_user_admin, name='edit_user_admin'),
    path('admin/users/delete/<int:id>', views.delete_user_admin, name='delete_user_admin'),
    
    path('admin/bookgroup/list/', views.list_lecture_group_admin, name='list_lecture_group_admin'),
    path('admin/bookgroup/add/', views.add_lecture_group_admin, name='add_lecture_group_admin'),
    path('admin/bookgroup/edit/<int:id>/', views.edit_lecture_group_admin, name='edit_lecture_group_admin'),
    path('admin/bookgroup/delete/<int:id>/', views.delete_lecture_group_admin, name='delete_lecture_group_admin'),
    path('admin/bookgroup/people/add/<int:id>', views.add_lecturer_admin, name='add_lecturer_admin'),
    path('admin/bookgroup/people/delete/<int:id>/', views.delete_lecturer_admin, name='delete_lecturer_admin'),
    path('admin/bookgroup/page/<int:id>', views.details_lg_admin, name='details_lg_admin'),

]