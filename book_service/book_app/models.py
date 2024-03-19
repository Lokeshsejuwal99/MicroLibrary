from django.db import models


class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    summary = models.TextField()
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13)
    pages = models.IntegerField()
    cover = models.TextField()

    def __str__(self):
        return self.title
