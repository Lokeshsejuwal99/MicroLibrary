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
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer

    def create(self, request, *args, **kwargs):
        data = BorrowRepository.create(self.serializer_class, request.data)
        return Response(
            {
                "success": True,
                "message": "Book Borrowed successfully",
                "data": data,
            },
            status=status.HTTP_201_CREATED,
        )
