from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for Book model."""
    list_display = ('id', 'title', 'author')
    list_filter = ('author',)
    search_fields = ('title', 'author')
    ordering = ('title',)