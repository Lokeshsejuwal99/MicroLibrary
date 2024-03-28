class BookRepository:
    @classmethod
    def create(cls, serializer, data):
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
