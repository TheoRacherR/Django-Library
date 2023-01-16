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
    path('book/borrow/list/', views.list_borrows, name='list_book_borrowed'),
    #user account
    path('bookgroup/add', views.add_lecture_group, name='add_lecture_group'),
    path('bookgroup/detail/<int:id>/', views.lg_page, name='lg_page'),
    # path('bookgroup/mylist/', views.list_lecture_group, name='list_lecture_group'),
    path('bookgroup/list/', views.list_lecture_groups, name='list_lecture_groups'),
    path('bookgroup/delete/<int:id>/', views.delete_lecture_group, name='delete_lecture_group'),
    path('bookgroup/people/add/<int:id>/', views.add_lecturer, name='add_lecturer'),
    path('bookgroup/people/delete/<int:id>/', views.delete_lecturer, name='delete_lecturer'),
    path('bookgroup/session/add/<int:id>/', views.add_lecture_group_details, name='add_lecture_group_details'),
    
    path('forum/list', views.list_forum, name='list_forum'),
    path('forum/add', views.add_forum, name='add_forum'),
    path('forum/delete/<int:id>/', views.delete_forum, name='delete_forum'),
    path('forum/page/<int:id>/', views.forum_page, name='forum_page'),
    path('forum/message/list/', views.list_own_message, name='list_own_message'),
    path('forum/message/add/<int:id>/', views.add_message, name='add_message'),
    path('forum/message/edit/<int:id>/', views.edit_message, name='edit_message'),
    path('forum/message/delete/<int:id>/', views.delete_message, name='delete_message'),




    #################
    ##### Admin #####
    #################
    path('admin/', views.admin, name='admin'),
    path('admin/set_role/id=<int:id>&role=<str:role>', views.set_role, name='set_role'), #admin

    path('admin/instance/add/<int:id>/', views.add_instance_admin, name='add_instance_admin'), #admin, bookseller
    path('admin/instance/delete/<int:id>/', views.delete_instance_admin, name='delete_instance_admin'), #admin, bookseller
    

    path('admin/book/add/', views.add_book_admin, name='add_book_admin'), #admin, bookseller
    path('admin/book/edit/<int:id>/', views.edit_book_admin, name='edit_book_admin'), #admin, bookseller
    path('admin/book/delete/<int:id>/', views.delete_book_admin, name='delete_book_admin'), #admin, bookseller
    path('admin/book/list/', views.list_books_admin, name='list_books_admin'), #admin, bookseller
    path('admin/book/page/<int:id>/', views.details_book_admin, name='book_page_admin'), #admin, bookseller
    path('admin/book/borrows/<int:id>/', views.borrow_book_admin, name='borrow_book_admin'), #admin, bookseller
    path('admin/book/borrows/cancel/<int:id>/', views.cancel_borrow_admin, name='cancel_borrow_admin'), #admin, bookseller
    path('admin/book/borrows/list/', views.list_borrows_admin, name='list_borrows_admin'), #admin, bookseller
    path('admin/book/collection/list/', views.list_collection_admin, name='list_collection_admin'), #admin, bookseller
    path('admin/book/collection/add/', views.add_collection_admin, name='add_collection_admin'), #admin, bookseller
    path('admin/book/collection/edit/<int:id>/', views.edit_collection_admin, name='edit_collection_admin'), #admin, bookseller
    path('admin/book/collection/delete/<int:id>/', views.delete_collection_admin, name='delete_collection_admin'), #admin, bookseller
    path('admin/book/genre/list/', views.list_genre_admin, name='list_genre_admin'), #admin, bookseller
    path('admin/book/genre/add/', views.add_genre_admin, name='add_genre_admin'), #admin, bookseller
    path('admin/book/genre/edit/<int:id>/', views.edit_genre_admin, name='edit_genre_admin'), #admin, bookseller
    path('admin/book/genre/delete/<int:id>/', views.delete_genre_admin, name='delete_genre_admin'), #admin, bookseller


    path('admin/library/add/', views.add_library_admin, name='add_library_admin'), #admin
    path('admin/library/delete/<int:id>/', views.delete_library_admin, name='delete_library_admin'), #admin
    path('admin/library/edit/<int:id>/', views.edit_library_admin, name='edit_library_admin'), #admin, bookseller
    path('admin/library/list/', views.list_libraries_admin, name='list_libraries_admin'), #admin, bookseller
    path('admin/library/page/<int:id>/', views.library_page_admin, name='library_page_admin'), #admin, bookseller


    path('admin/users/list/', views.list_users_admin, name='list_users_admin'), #admin, bookseller
    path('admin/users/edit/<int:id>/', views.edit_user_admin, name='edit_user_admin'), #admin
    path('admin/users/delete/<int:id>/', views.delete_user_admin, name='delete_user_admin'), #admin
    path('admin/users/page/<int:id>/', views.page_user, name='page_user'), #admin, bookseller
    

    path('admin/bookgroup/list/', views.list_lecture_group_admin, name='list_lecture_group_admin'), #admin, bookseller
    path('admin/bookgroup/add/', views.add_lecture_group_admin, name='add_lecture_group_admin'), #admin
    path('admin/bookgroup/edit/<int:id>/', views.edit_lecture_group_admin, name='edit_lecture_group_admin'), #admin
    path('admin/bookgroup/delete/<int:id>/', views.delete_lecture_group_admin, name='delete_lecture_group_admin'), #admin
    path('admin/bookgroup/people/add/<int:id>/', views.add_lecturer_admin, name='add_lecturer_admin'), #admin
    path('admin/bookgroup/people/delete/<int:id>/', views.delete_lecturer_admin, name='delete_lecturer_admin'), #admin
    path('admin/bookgroup/page/<int:id>/', views.details_lg_admin, name='details_lg_admin'), #admin, bookseller


    path('admin/forum/page/<int:id>/', views.forum_page_admin, name="forum_page_admin"), #admin, bookseller
    path('admin/forum/list/', views.list_forum_admin, name="list_forum_admin"), #admin, bookseller
    path('admin/forum/add/', views.add_forum_admin, name="add_forum_admin"), #admin, bookseller
    path('admin/forum/edit/<int:id>/', views.edit_forum_admin, name="edit_forum_admin"), #admin, bookseller
    path('admin/forum/delete/<int:id>/', views.delete_forum_admin, name="delete_forum_admin"), #admin, bookseller
    path('admin/forum/message/list/<int:id>/', views.list_message_admin, name="list_message_admin"), #admin, bookseller
    path('admin/forum/message/edit/<int:id>/', views.edit_message_admin, name="edit_message_admin"), #admin, bookseller
    path('admin/forum/message/delete/<int:id>/', views.delete_message_admin, name="delete_forum_admin"), #admin, bookseller


]