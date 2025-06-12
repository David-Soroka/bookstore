from django import forms
from .models import Author, Book

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'birth_year',]

# Форма для книги з ручним введенням автора
class BookForm(forms.ModelForm):
    author_name = forms.CharField(label="Ім’я автора")
    author_birth_year = forms.IntegerField(label="Рік народження автора")

    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'genre', 'price', 'is_available']