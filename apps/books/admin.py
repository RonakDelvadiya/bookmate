from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'number_of_pages']
    search_fields = ['title', 'author']
    list_filter = ['created_at', 'last_modified_at']
    
    def save_model(self, request, obj, form, change):
        if change and 'title' in form.changed_data:
            updated_details = Book._fetch_book_details(obj.title)
            obj.author = updated_details['author']
            obj.number_of_pages = updated_details['number_of_pages']
        super().save_model(request, obj, form, change)