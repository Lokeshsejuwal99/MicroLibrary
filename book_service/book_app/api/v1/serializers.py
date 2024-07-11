from rest_framework import serializers
from book_app.models import Books


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = "__all__"
