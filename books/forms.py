from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Author, Book
from django.utils.translation import gettext_lazy as _

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'birth_year']
        labels = {
            'name': _('Author Name'),
            'birth_year': _('Year of Birth'),
        }

class BookForm(forms.ModelForm):
    author_name = forms.CharField(label=_("Author Name"))
    author_birth_year = forms.IntegerField(label=_("Author Birth Year"))

    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'genre', 'price', 'is_available']
        labels = {
            'title': _('Title'),
            'publication_year': _('Publication Year'),
            'genre': _('Genre'),
            'price': _('Price'),
            'is_available': _('Available'),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label=_("Email"))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'password1': _('Password'),
            'password2': _('Confirm Password'),
        }
