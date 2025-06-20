from django.contrib import admin
from .models import Author, Book
from django.utils.translation import gettext_lazy as _

admin.site.site_header = "Bookstore – Адмінпанель"
admin.site.site_title = "Bookstore"
admin.site.index_title = "Управління контентом"

class BookInline(admin.TabularInline):  # для редагування книг у автора
    model = Book
    extra = 1


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_year')
    search_fields = ('name',)
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'genre', 'price', 'is_available')
    list_filter = ('genre', 'publication_year', 'is_available')
    search_fields = ('title', 'author__name')
    actions = ['mark_as_available', 'mark_as_unavailable']

    @admin.action(description='Позначити як доступні')
    def mark_as_available(self, request, queryset):
        queryset.update(is_available=True)

    @admin.action(description='Позначити як недоступні')
    def mark_as_unavailable(self, request, queryset):
        queryset.update(is_available=False)
