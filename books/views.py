from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from .forms import AuthorForm, BookForm, RegisterForm
from .models import Author, Book, UserProfile
from .services import get_all_books
from django.utils.timezone import now
from django.utils.translation import gettext as _
import datetime

def role_required(roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            try:
                if request.user.userprofile.role not in roles:
                    return HttpResponseForbidden(_("⛔ Доступ заборонено"))
            except UserProfile.DoesNotExist:
                return HttpResponseForbidden(_("⛔ Профіль користувача не знайдено"))
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def home_redirect(request):
    return redirect('login')  # де у шаблоні буде меню для входу / реєстрації

def logout_view(request):
    login_time = request.session.get('login_time')
    if login_time:
        login_dt = datetime.datetime.fromisoformat(login_time)
        duration = now() - login_dt
        print(f'Користувач {request.user.username} був у системі: {duration}')
        # Можна зберігати в БД або лог-файл тут
    logout(request)
    return redirect('login')


# --------- Author Views (Class-Based) ---------

@method_decorator(role_required(['manager', 'admin']), name='dispatch')
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


@method_decorator(role_required(['manager', 'admin']), name='dispatch')
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


@method_decorator(role_required(['manager', 'admin']), name='dispatch')
class AuthorDeleteView(View):
    def get(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        return render(request, 'books/author_confirm_delete.html', {'author': author})

    def post(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        author.delete()
        return redirect('author_list')


class AuthorListView(View):
    @method_decorator(login_required)
    def get(self, request):
        authors = Author.objects.all()
        return render(request, 'books/author_list.html', {'authors': authors})


# --------- Book Views (Class-Based) ---------

@method_decorator(login_required, name='dispatch')
class BookListView(View):
    def get(self, request):
        # Записуємо час входу для user і manager
        try:
            if request.user.userprofile.role in ['user', 'manager']:
                request.session['login_time'] = str(now())
        except UserProfile.DoesNotExist:
            pass  # Якщо профіль відсутній — ігноруємо

        books = get_all_books()
        return render(request, 'books/book_list.html', {'books': books})


@method_decorator(role_required(['manager', 'admin']), name='dispatch')
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


@method_decorator(role_required(['manager', 'admin']), name='dispatch')
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


@method_decorator(role_required(['manager', 'admin']), name='dispatch')
class BookDeleteView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'books/book_confirm_delete.html', {'book': book})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return redirect('book_list')


class BookDetailView(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'books/book_detail.html', {'book': book})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
        return render(request, 'registration/register.html', {'form': form})
