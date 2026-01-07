from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to retrieve list of all books.
    
    This view provides a read-only endpoint that returns
    a list of all Book instances in the database.
    
    Endpoint: GET /api/books/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Book instances.
    
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update`, `partial_update`, and `destroy` actions.
    
    Endpoints:
        GET /api/books_all/ - List all books
        POST /api/books_all/ - Create a new book
        GET /api/books_all/{id}/ - Retrieve a book
        PUT /api/books_all/{id}/ - Update a book
        PATCH /api/books_all/{id}/ - Partial update a book
        DELETE /api/books_all/{id}/ - Delete a book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer