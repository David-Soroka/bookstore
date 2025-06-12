from .models import Book, Author

def get_all_books():
    return Book.objects.select_related('author').all()

def get_books_by_author(author_id):
    return Book.objects.filter(author_id=author_id)

def get_available_books():
    return Book.objects.filter(is_available=True)
