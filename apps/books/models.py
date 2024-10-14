from __future__ import unicode_literals
from django.utils.translation import gettext_lazy as _
from django.db import models
from utils.models import CommonFieldModel, User
import requests
from .utils import FetchBookDetailsFromIsbndb, fetch_book_details_from_isbndb


class Book(CommonFieldModel):
    """
    Represents a book in the system.

    This model stores information about books, including their title, author, and number of pages.
    It extends the CommonFieldModel, which likely provides common fields like creation and modification timestamps.

    Attributes:
        title (CharField): The title of the book. Max length 255, required, and unique.
        author (CharField): The author of the book. Max length 255, optional.
        number_of_pages (PositiveIntegerField): The number of pages in the book. Optional.
        created_by (ForeignKey): The user who created this book record. Optional, set to NULL on user deletion.
        last_modified_by (ForeignKey): The user who last modified this book record. Optional, set to NULL on user deletion.

    Methods:
        _fetch_book_details(cls, title): Class method to fetch book details from OpenLibrary API.
        save(**kwargs): Overridden to automatically fetch and set book details if missing.
        __str__(): Returns the string representation of the book (its title or ID).
        __repr__(): Returns a detailed string representation for debugging.

    Behavior:
        - On save, if author or number_of_pages is missing, it attempts to fetch these details from OpenLibrary API.
        - If fetching fails, it uses default values (Unknown author, random number of pages).

    Meta:
        db_table: "books_book"
        verbose_name: "Book"
        verbose_name_plural: "Books"

    Note:
        This model uses Django's translation system for internationalization of help texts and verbose names.
    """

    title = models.CharField(max_length=255, blank=False, null=False, unique=True, help_text=_("The title of the book. Must be unique."))
    author = models.CharField(max_length=255, null=True, blank=True, help_text=_("The author of the book. Can be left blank."))
    number_of_pages = models.PositiveIntegerField(null=True, blank=True, help_text=_("The number of pages in the book. Can be left blank."))
    is_rented = models.BooleanField(default=False, help_text=_("Whether the book is rented or not."))
    created_by = models.ForeignKey(User, related_name='book_created_by', on_delete=models.SET_NULL, null=True, blank=True, help_text=_("The user who created this book record."))
    last_modified_by = models.ForeignKey(User, related_name='book_modified_by', on_delete=models.SET_NULL, null=True, blank=True, help_text=_("The user who last modified this book record."))


    @classmethod
    def _fetch_book_details(cls, title) -> FetchBookDetailsFromIsbndb :
        try:
            return fetch_book_details_from_isbndb(title)
        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"Error fetching book details: {e}")
        return FetchBookDetailsFromIsbndb()
        
    class Meta:
        db_table = "books_book"
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    def __str__(self):
        return str(self.title) if self.title else self.id
    
    def save(self, **kwargs):
        if not self.author or not self.number_of_pages:
            try:
                book_details = self._fetch_book_details(self.title)
                self.author = book_details.author if not self.author else self.author
                self.number_of_pages = book_details.number_of_pages if not self.number_of_pages else self.number_of_pages
                self.title = f"{self.title} | {book_details.title}"
            except Exception as e:
                print(f"An error occurred while fetching or processing book details: {e}")
        super(Book, self).save(**kwargs)
    
    # for better object representation in debugging
    def __repr__(self):
        return f"<Book: {self.title}>"