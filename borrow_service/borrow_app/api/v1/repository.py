class BorrowRepository:
    @classmethod
    def create(cls, serializer, data):
        serializer_instance = serializer(data=data)
        serializer_instance.is_valid(raise_exception=True)
        serializer_instance.save()
        return serializer_instance.data
