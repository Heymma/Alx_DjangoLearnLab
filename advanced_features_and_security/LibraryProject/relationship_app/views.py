from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test

from .models import Book
from .models import Library
from .models import UserProfile


# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view: show details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


# Authentication views

class CustomLoginView(LoginView):
    template_name = "relationship_app/login.html"


class CustomLogoutView(LogoutView):
    template_name = "relationship_app/logout.html"


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


# Role check helper functions

def is_admin(user):
    return (
        user.is_authenticated
        and hasattr(user, "userprofile")
        and user.userprofile.role == "Admin"
    )


def is_librarian(user):
    return (
        user.is_authenticated
        and hasattr(user, "userprofile")
        and user.userprofile.role == "Librarian"
    )


def is_member(user):
    return (
        user.is_authenticated
        and hasattr(user, "userprofile")
        and user.userprofile.role == "Member"
    )


# Role-based views

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse


@permission_required("relationship_app.can_add_book")
def add_book(request):
    return HttpResponse("Book added successfully.")


@permission_required("relationship_app.can_change_book")
def edit_book(request, pk):
    return HttpResponse("Book edited successfully.")


@permission_required("relationship_app.can_delete_book")
def delete_book(request, pk):
    return HttpResponse("Book deleted successfully.")