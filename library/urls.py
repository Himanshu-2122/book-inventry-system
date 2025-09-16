from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  
  path('register', views.Registers, name='register'),
  path("login/", views.Login, name="login"),

 
  path('logout', views.logout, name='logout'),



    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),


    # Borrow/Return
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:transaction_id>/', views.return_book, name='return_book'),
    path('my-borrowed/', views.my_borrowed_books, name='my_borrowed_books'),

    path('profile/', views.profile, name='profile'),



    
]