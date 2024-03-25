from django.urls import path
from .views import BooksView, BookDetailView, BorrowBookView

urlpatterns = [
    path("books", BooksView.as_view(), name="books"),
    path("book-detail/<int:pk>/", BookDetailView.as_view(), name="BookDetail"),
    path("borrow-book/", BorrowBookView.as_view(), name="BorrowBookView"),
]
