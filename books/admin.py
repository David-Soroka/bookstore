from django.contrib import admin
from .models import Author, Book
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .models import UserProfile

admin.site.site_header = _("Bookstore – Admin Panel")
admin.site.site_title = _("Bookstore")
admin.site.index_title = _("Content Management")

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

    @admin.action(description=_('Mark as available'))
    def mark_as_available(self, request, queryset):
        queryset.update(is_available=True)

    @admin.action(description=_('Mark as unavailable'))
    def mark_as_unavailable(self, request, queryset):
        queryset.update(is_available=False)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
