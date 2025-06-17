from django.shortcuts import redirect, render, get_object_or_404
from django.views import View

from .forms import AuthorForm, BookForm
from .models import Author, Book
from .services import get_all_books


def home_redirect(request):
    return redirect('book_list')


# --------- Author Views (Class-Based) ---------

class AuthorListView(View):
    def get(self, request):
        authors = Author.objects.all()
        return render(request, 'books/author_list.html', {'authors': authors})


class AuthorCreateView(View):
    def get(self, request):
        form = AuthorForm()
        return render(request, 'books/author_form.html', {'form': form})

    def post(self, request):
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
        return render(request, 'books/author_form.html', {'form': form})


class AuthorUpdateView(View):
    def get(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        form = AuthorForm(instance=author)
        return render(request, 'books/author_form.html', {'form': form})

    def post(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_list')
        return render(request, 'books/author_form.html', {'form': form})


class AuthorDeleteView(View):
    def get(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        return render(request, 'books/author_confirm_delete.html', {'author': author})

    def post(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        author.delete()
        return redirect('author_list')


# --------- Book Views (Class-Based) ---------

class BookListView(View):
    def get(self, request):
        books = get_all_books()
        return render(request, 'books/book_list.html', {'books': books})


class BookCreateView(View):
    def get(self, request):
        form = BookForm()
        return render(request, 'books/book_form.html', {'form': form})

    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            author_name = form.cleaned_data['author_name'].strip()
            author_birth_year = form.cleaned_data['author_birth_year']

            author, _ = Author.objects.get_or_create(
                name=author_name,
                defaults={'birth_year': author_birth_year}
            )

            book = form.save(commit=False)
            book.author = author
            book.save()
            return redirect('book_list')
        return render(request, 'books/book_form.html', {'form': form})


class BookUpdateView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(instance=book)
        return render(request, 'books/book_form.html', {'form': form})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
        return render(request, 'books/book_form.html', {'form': form})


class BookDeleteView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'books/book_confirm_delete.html', {'book': book})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return redirect('book_list')


class BookDetailView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'books/book_detail.html', {'book': book})
