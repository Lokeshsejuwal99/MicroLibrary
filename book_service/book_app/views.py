from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Books
from .serializers import BooksSerializer
from rest_framework import status


class BooksView(APIView):
    def get(self, request):
        books = Books.objects.all()
        serializer = BooksSerializer(books, many=True)
        return Response(
            {
                "success": True,
                "message": "Books fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Book created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"success": False, "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
