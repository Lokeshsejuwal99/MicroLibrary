from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

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


class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    # lookup_field = "id"

    def retrieve(self, request, user_id, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "success": True,
                "message": "Books retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def update(self, request, user_id, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(
                    {"success": False, "error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Book Updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            data = {"success": False, "message": str(e)}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, user_id, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            data = {"success": True, "message": "Book deleted successfully"}
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            data = {"success": False, "message": str(e)}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
