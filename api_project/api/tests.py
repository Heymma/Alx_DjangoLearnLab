from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import Book


class AuthenticationTestCase(APITestCase):
    """Test cases for API authentication."""
    
    def setUp(self):
        """Set up test data."""
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        # Use get_or_create to avoid duplicate token error
        # (in case a signal auto-creates tokens)
        self.token, created = Token.objects.get_or_create(user=self.user)
        
        # Create a test book
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author'
        )
        
        self.list_url = reverse('book-list')
        self.token_url = reverse('api_token_auth')
    
    def test_unauthenticated_request_denied(self):
        """Test that unauthenticated requests are denied."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authenticated_request_allowed(self):
        """Test that authenticated requests are allowed."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_obtain_token(self):
        """Test obtaining auth token with valid credentials."""
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_obtain_token_invalid_credentials(self):
        """Test that invalid credentials don't return a token."""
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookViewSetAuthenticationTestCase(APITestCase):
    """Test cases for BookViewSet with authentication."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Use get_or_create to avoid duplicate token error
        self.token, created = Token.objects.get_or_create(user=self.user)
        
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author'
        )
        
        self.list_url = reverse('book_all-list')
        self.detail_url = reverse('book_all-detail', kwargs={'pk': self.book.pk})
    
    def test_list_books_authenticated(self):
        """Test listing books with authentication."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_book_authenticated(self):
        """Test creating a book with authentication."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.list_url, {
            'title': 'New Book',
            'author': 'New Author'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_book_unauthenticated(self):
        """Test that creating a book without auth fails."""
        response = self.client.post(self.list_url, {
            'title': 'New Book',
            'author': 'New Author'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_book_authenticated(self):
        """Test updating a book with authentication."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.put(self.detail_url, {
            'title': 'Updated Book',
            'author': 'Updated Author'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_book_authenticated(self):
        """Test deleting a book with authentication."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)