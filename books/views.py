from django.shortcuts import render, get_object_or_404, redirect
from .models import Author, Book
from .forms import AuthorForm, BookForm
from .services import get_all_books
from django.shortcuts import redirect

# Author views
def author_list(request):
    authors = Author.objects.all()
    return render(request, 'books/author_list.html', {'authors': authors})

def author_create(request):
    form = AuthorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('author_list')
    return render(request, 'books/author_form.html', {'form': form})

def author_update(request, pk):
    author = get_object_or_404(Author, pk=pk)
    form = AuthorForm(request.POST or None, instance=author)
    if form.is_valid():
        form.save()
        return redirect('author_list')
    return render(request, 'books/author_form.html', {'form': form})

def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        author.delete()
        return redirect('author_list')
    return render(request, 'books/author_confirm_delete.html', {'author': author})

# Book views
def book_list(request):
    books = get_all_books()
    return render(request, 'books/book_list.html', {'books': books})

def book_create(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'books/book_form.html', {'form': form})

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'books/book_form.html', {'form': form})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})

def home_redirect(request):
    return redirect('book_list')