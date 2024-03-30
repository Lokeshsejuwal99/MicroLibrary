from django.contrib import admin
from django.urls import path, include
from .views import BorrowBookView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"borrow-book", BorrowBookView, basename="borrow-book")


urlpatterns = [
    path("", include(router.urls)),
]
