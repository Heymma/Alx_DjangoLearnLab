"""
API Views for the Book model.

Authentication: Token Authentication is required for all endpoints.
Permissions: All endpoints require authenticated users.

Views:
    BookList: List all books (GET only)
    BookViewSet: Full CRUD operations on books
"""

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to retrieve list of all books.
    
    * Requires token authentication.
    * Only authenticated users can access this view.
    
    Endpoint: GET /api/books/
    
    Returns:
        List of all books in JSON format
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Book instances.
    
    * Requires token authentication.
    * Only authenticated users can perform any action.
    
    Endpoints:
        GET /api/books_all/ - List all books
        POST /api/books_all/ - Create a new book
        GET /api/books_all/{id}/ - Retrieve a specific book
        PUT /api/books_all/{id}/ - Update a book (full)
        PATCH /api/books_all/{id}/ - Update a book (partial)
        DELETE /api/books_all/{id}/ - Delete a book
    
    Permissions:
        All actions require authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]