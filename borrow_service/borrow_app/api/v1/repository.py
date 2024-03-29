class BorrowRepository:
    @classmethod
    def create(cls, serializer, data):
        serializer_instance = serializer(data=data)
        serializer_instance.is_valid(raise_exception=True)
        serializer_instance.save()
        return serializer_instance.data

    @classmethod
    def update(cls, instance, data):
        serializer_instance = instance.get_serializer(instance, data=data, partial=True)
        serializer_instance.is_valid(raise_exception=True)
        serializer_instance.save()
        return serializer_instance.data

    @classmethod
    def delete_borrowed(cls, instance):
        instance.delete()
        return True
