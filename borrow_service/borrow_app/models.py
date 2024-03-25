from django.db import models
from django.utils import timezone


class Borrow(models.Model):
    # user_id = models.UUIDField()  # External identifier for the user
    # book_id = models.UUIDField()  # External identifier for the book
    user_id = models.IntegerField()
    book_id = models.IntegerField()
    borrow_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    returned = models.BooleanField(default=False)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.book_id + self.user_id
