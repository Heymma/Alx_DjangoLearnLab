from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm


@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()  # Secure ORM query (no SQL injection risk)
    return render(request, "bookshelf/book_list.html", {"books": books})


def secure_form_view(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()  # Secure save with validation (sanitizes input)
            return render(request, "bookshelf/form_example.html", {"form": form, "message": "Saved securely"})
    else:
        form = BookForm()
    return render(request, "bookshelf/form_example.html", {"form": form})