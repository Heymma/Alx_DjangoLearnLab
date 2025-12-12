from .models import Author, Book, Library, Librarian


def get_books_by_author(author_name: str):
    """
    Query all books by a specific author.
    """
    return Book.objects.filter(author__name=author_name)


def get_books_in_library(library_name: str):
    """
    List all books in a given library.
    """
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return Book.objects.none()
    return library.books.all()


def get_librarian_for_library(library_name: str):
    """
    Retrieve the librarian for a given library.
    """
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return None
    # thanks to related_name="librarian" we can access it like this:
    return library.librarian