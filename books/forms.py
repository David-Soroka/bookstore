from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Author, Book

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'birth_year',]

# Форма для книги з ручним введенням автора
class BookForm(forms.ModelForm):
    author_name = forms.CharField(label="Name author")
    author_birth_year = forms.IntegerField(label="Author birth year")

    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'genre', 'price', 'is_available']

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']