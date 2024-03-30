from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from borrow_app.models import Borrow
from borrow_app.borrow_book_producer import BookProducer
from .repository import BorrowRepository
from .serializers import BorrowSerializer


# Create your views here.
class BorrowBookView(ModelViewSet):
    """
    View for handling book borrowing operations.
    """

    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = BorrowRepository.create(self.serializer_class, request.data)
            BookProducer(
                request.data["book_id"]
            )  # Publish the book request to the RabbitMQ
            return Response(
                {
                    "success": True,
                    "message": "Book Borrowed successfully",
                    "data": data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Error Borrowing book",
                    "error": str(e),  # Include the error message in the response
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
