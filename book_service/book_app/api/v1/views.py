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
    """
    View for handling book operations.
    """

    queryset = Books.objects.all()
    serializer_class = BooksSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = BookRepository.create(self.serializer_class, request.data)
            return Response(
                {
                    "success": True,
                    "message": "Book created successfully",
                    "data": data,  # Include serialized data of the created instance in the response
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Error creating book",
                    "error": str(e),  # Include the error message in the response
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            data = BookRepository.update(instance, request.data)
            return Response(
                {
                    "success": True,
                    "message": "Book updated successfully",
                    "data": data,  # Include serialized data of the updated instance in the response
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Error updating book",
                    "error": str(e),  # Include the error message in the response
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            BookRepository.delete_book(instance)
            return Response(
                {
                    "success": True,
                    "message": "Book deleted successfully",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Error deleting book",
                    "error": str(e),  # Include the error message in the response
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
