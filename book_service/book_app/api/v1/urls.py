from django.urls import path, include
from .views import BooksView, BookDetailView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("books", BooksView, basename="books")


urlpatterns = [
    path("", include(router.urls)),
    path("book-detail/<int:pk>/", BookDetailView.as_view(), name="BookDetail"),
]
