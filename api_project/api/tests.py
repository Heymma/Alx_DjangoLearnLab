from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book


class BookViewSetTestCase(APITestCase):
    """Test cases for BookViewSet CRUD operations."""
    
    def setUp(self):
        """Set up test data."""
        self.book1 = Book.objects.create(
            title="Test Book 1",
            author="Test Author 1"
        )
        self.book2 = Book.objects.create(
            title="Test Book 2",
            author="Test Author 2"
        )
        self.list_url = reverse('book_all-list')
        self.detail_url = reverse('book_all-detail', kwargs={'pk': self.book1.pk})
    
    def test_list_books(self):
        """Test GET /api/books_all/ - List all books."""
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_create_book(self):
        """Test POST /api/books_all/ - Create a new book."""
        data = {
            'title': 'New Test Book',
            'author': 'New Test Author'
        }
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], 'New Test Book')
    
    def test_retrieve_book(self):
        """Test GET /api/books_all/{id}/ - Retrieve a book."""
        response = self.client.get(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book 1')
        self.assertEqual(response.data['author'], 'Test Author 1')
    
    def test_update_book(self):
        """Test PUT /api/books_all/{id}/ - Update a book."""
        data = {
            'title': 'Updated Book Title',
            'author': 'Updated Author'
        }
        response = self.client.put(self.detail_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')
    
    def test_partial_update_book(self):
        """Test PATCH /api/books_all/{id}/ - Partial update a book."""
        data = {'title': 'Partially Updated Title'}
        response = self.client.patch(self.detail_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Title')
        self.assertEqual(self.book1.author, 'Test Author 1')  # Unchanged
    
    def test_delete_book(self):
        """Test DELETE /api/books_all/{id}/ - Delete a book."""
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())
    
    def test_retrieve_nonexistent_book(self):
        """Test GET /api/books_all/{id}/ - Book not found."""
        url = reverse('book_all-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_book_invalid_data(self):
        """Test POST with invalid data."""
        data = {'title': ''}  # Empty title and missing author
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookListViewTestCase(APITestCase):
    """Test cases for the original BookList view."""
    
    def setUp(self):
        """Set up test data."""
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author"
        )
        self.url = reverse('book-list')
    
    def test_list_books(self):
        """Test GET /api/books/ - Original list endpoint."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)