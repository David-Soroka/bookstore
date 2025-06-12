from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    birth_year = models.PositiveIntegerField()
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=200)
    publication_year = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
