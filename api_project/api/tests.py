from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book


class BookAPITestCase(APITestCase):
    """Test cases for the Book API endpoints."""
    
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
        self.url = reverse('book-list')
    
    def test_get_all_books(self):
        """Test retrieving all books."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_book_list_content(self):
        """Test that book list contains correct data."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check first book data
        titles = [book['title'] for book in response.data]
        self.assertIn('Test Book 1', titles)
        self.assertIn('Test Book 2', titles)
    
    def test_empty_book_list(self):
        """Test retrieving books when database is empty."""
        Book.objects.all().delete()
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)