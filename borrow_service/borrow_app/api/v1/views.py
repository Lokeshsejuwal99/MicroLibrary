from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .repository import BorrowRepository
from rest_framework.viewsets import ModelViewSet

from rest_framework.response import Response
from borrow_app.models import Borrow
from .serializers import BorrowSerializer
from rest_framework import status


# Create your views here.
class BorrowBookView(ModelViewSet):
    """
    View for handling book borrowing operations.
    """

    def create(self, request, *args, **kwargs):
        try:
            data = BorrowRepository.create(self.serializer_class, request.data)
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
