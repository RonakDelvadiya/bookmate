from django import forms
from django.contrib import admin
from .models import Book
from django.contrib.auth import get_user_model
User = get_user_model()

class BookAdminForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_by'].queryset = User.objects.filter(is_staff=True, is_active=True)
        self.fields['last_modified_by'].queryset = User.objects.filter(is_staff=True, is_active=True)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
    list_display = ['title', 'author', 'number_of_pages', "is_rented"]
    search_fields = ['title', 'author']
    list_filter = ['created_at', 'last_modified_at']
    
    def save_model(self, request, obj, form, change):
        if change and 'title' in form.changed_data:
            updated_details = Book._fetch_book_details(obj.title)
            obj.author = updated_details.author
            obj.number_of_pages = updated_details.number_of_pages
            obj.title = f"{obj.title} | {updated_details.title}"
        super().save_model(request, obj, form, change)