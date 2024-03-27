from django.contrib import admin
from django.urls import path
from .views import BorrowBookView

urlpatterns = [
    path("borrow-book/", BorrowBookView.as_view(), name="BorrowBookView"),
]
