from django.db import models


class Book(models.Model):
    """
    Book model representing a book in the library.
    
    Attributes:
        title (str): The title of the book (max 200 characters)
        author (str): The author of the book (max 100 characters)
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'