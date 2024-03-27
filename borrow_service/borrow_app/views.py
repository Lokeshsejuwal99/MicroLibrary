from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from rest_framework.response import Response
from .models import Books
from .serializers import BooksSerializer
from rest_framework import status


# Create your views here.
class BorrowBookView(APIView):

    def post(self, request):
        print(request.data)

        # BookProducer(request.data)
        return Response(
            {"success": True, "error": "serializer.errors"},
            status=status.HTTP_400_BAD_REQUEST,
        )
