from django.urls import path
from .views import BooksView, BookDetailView

urlpatterns = [
    path("books/", BooksView.as_view(), name="books"),
    path("book-detail/", BookDetailView.as_view(), name="BookDetail"),
]
