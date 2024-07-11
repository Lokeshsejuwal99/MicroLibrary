from django.db import models
from django.utils import timezone


class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    summary = models.TextField()
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13)
    pages = models.IntegerField()
    cover = models.TextField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Borrow(models.Model):
    user_id = models.IntegerField()
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    returned = models.BooleanField(default=False)
    return_date = models.DateTimeField(null=True, blank=True)


