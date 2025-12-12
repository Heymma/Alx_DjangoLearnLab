from .models import Author, Book, Library, Librarian


def get_books_by_author(author_name: str):
    """
    Query all books by a specific author.
    """
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)


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

    librarian = Librarian.objects.get(library=library)
    return librarian