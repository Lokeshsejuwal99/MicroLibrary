from django.contrib import admin
from .models import Books


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "isbn")
    search_fields = ("title", "author", "isbn")
    list_filter = ("title", "author")
    list_per_page = 10
    ordering = ("title", "author", "isbn")
    list_display_links = ("title", "author", "isbn")
    # list_editable = ("quantity",)


# Register your models here.
