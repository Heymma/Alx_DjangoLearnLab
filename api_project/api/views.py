from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to retrieve list of all books.
    
    This view provides a read-only endpoint that returns
    a list of all Book instances in the database.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer