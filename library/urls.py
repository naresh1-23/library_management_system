from django.urls import path
from . import views

urlpatterns = [
    path("books_list/", views.BookView.as_view(), name = "book_lists"),
    path("booksdetail_list/", views.BookDetailView.as_view(), name = "book_lists"),
    path("bookdetail/<int:pk>/", views.BookDetailUpdateDeleteView.as_view(), name = "book"),
    path("users/", views.UserLists.as_view(), name = "users"),
    path("user_detail/<int:pk>/", views.UserUpdateDeleteView.as_view(), name = "user-detail"),
    path("book_borrowers/", views.BookBorrowLists.as_view(), name = "book-borrowers"),
    path("borrow/<int:pk>/", views.BorrowUpdateDeleteView.as_view(), name = "borrow"),
    path("login/", views.LoginView.as_view(), name = 'login')
]