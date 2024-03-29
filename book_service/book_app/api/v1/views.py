from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from rest_framework import status
from book_app.models import Books
from .serializers import BooksSerializer

# from .bookProducer import BookProducer
from .repository import BookRepository


class BooksView(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer

    def create(self, request, *args, **kwargs):
        data = BookRepository.create(self.serializer_class, request.data)
        return Response(
            {
                "success": True,
                "message": "Book created successfully",
            },
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, *args, **kwargs):
        data = BookRepository.update(self, request, *args, **kwargs)
        return Response(
            {
                "success": True,
                "message": "Book updated successfully",
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, book_id):
        BookRepository.delete_book(self, book_id)
        return Response(
            {
                "success": True,
                "message": "Book deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
