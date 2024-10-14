from __future__ import unicode_literals
from django.utils.translation import gettext_lazy as _
from books.models import Book
from utils.models import CommonFieldModel
from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.utils import timezone
from bookmate.load_env_vars import var_settings
from django.core.exceptions import ValidationError
import math

User = get_user_model()

class Rental(CommonFieldModel):
    """
    Represents a book rental in the system.

    Attributes:
        student (ForeignKey): The user who rented the book.
        book (ForeignKey): The book that was rented.
        rental_date (DateTimeField): When the book was rented.
        return_date (DateTimeField): When the book was returned (nullable).
        returned (BooleanField): Whether the book has been returned.
        created_by (ForeignKey): User who created this record.
        last_modified_by (ForeignKey): User who last modified this record.

    Methods:
        clean(): Validates the model before saving.
        save(*args, **kwargs): Custom save logic for return status.
        _rental_duration(): Calculates rental duration in days.
        _rental_fee(): Calculates rental fee based on duration.

    Validation:
        - Return date must be after rental date and not in the future.

    Save Behavior:
        - Sets 'returned' to True when a valid return_date is provided.
        - Handles both creation and update scenarios.

    Exceptions:
        ValidationError: For invalid dates.
        Book.DoesNotExist, User.DoesNotExist: For missing related objects.

    Meta:
        db_table: "rentals_rental"
        verbose_name: "Rental"
        verbose_name_plural: "Rentals"
    """

    student = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, help_text=_("The student who rented the book."))
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False, blank=False, help_text=_("The book that was rented."))
    rental_date = models.DateTimeField(default=timezone.now, null=False, blank=False, help_text=_("The date and time when the book was rented."))
    return_date = models.DateTimeField(null=True, blank=True, help_text=_("The date and time when the book was returned. Leave blank if not yet returned."))
    returned = models.BooleanField(default=False, help_text=_("Indicates whether the book has been returned. If returned date is provided, it will be set to True automatically."))
    created_by = models.ForeignKey(User, related_name='rental_created_by', on_delete=models.SET_NULL, null=True, blank=True, help_text=_("The user who created this rental record."))
    last_modified_by = models.ForeignKey(User, related_name='rental_modified_by', on_delete=models.SET_NULL, null=True, blank=True, help_text=_("The user who last modified this rental record."))

    def _rental_duration(self):
        """
        Calculates the rental duration in days.
        Returns:
            int: The number of days the book has been rented.
        Raises:
            ValueError: If the return date is earlier than the rental date.
        """
        end_date = self.return_date if self.return_date else timezone.now()
        if end_date < self.rental_date :
            print("Return date cannot be earlier than rental date.")
            return 0
        return (end_date.date() - self.rental_date.date()).days

    def _rental_fee(self):
        """
        Calculates the rental fee after the free rental period.
        Returns:
            float: The calculated rental fee.
        Raises:
            Book.DoesNotExist: If the associated book is not found.
        """
        try:
            free_period = var_settings.FREE_RENTAL_PERIOD  # Free period in days
            duration = self._rental_duration()
            if duration > free_period:
                extra_days = duration - free_period
                return math.ceil(extra_days / 30) * (self.book.number_of_pages / 100)
            return 0.0
        except Exception as e:
            print(f"Error calculating rental fee: {e}")
            return 0

    def clean(self):
        """
        Validates the model before saving.
        Raises:
            ValidationError: If validation fails.
        """
        if self.return_date:
            if self.return_date < self.rental_date:
                raise ValidationError("Return date cannot be earlier than rental date.")
            
            if self.return_date > timezone.now():
                raise ValidationError("Return date cannot be in the future.")
    
    @transaction.atomic
    def delete(self, *args, **kwargs):
        self.book.is_rented = False # Update the book's is_rented status before deleting the rental
        self.book.save()        
        super().delete(*args, **kwargs)

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.clean()

        # Check if this is an update operation
        update_fields = kwargs.get('update_fields')

        # Automatically set returned based on the presence and validity of return_date
        if self.return_date and self.return_date <= timezone.now() and self.return_date >= self.rental_date:
            self.returned = True
            self.book.is_rented = False
            self.book.save()
        else:
            self.returned = False
            self.book.is_rented = True
            self.book.save()

        is_update = self.pk is not None
        if is_update:
            original_rental = Rental.objects.get(pk=self.pk)
            old_book = original_rental.book

            if is_update and old_book != self.book:
                old_book.is_rented = False
                old_book.save()

        # If this is an update operation, add 'returned' to update_fields
        if update_fields is not None:
            update_fields = set(update_fields)
            update_fields.add('returned')
            kwargs['update_fields'] = update_fields

        super().save(*args, **kwargs)

    def __str__(self):
        username = self.student.username or self.student.email
        book_title = self.book.title
        return f"{username} -> {book_title}"

    class Meta:
        db_table = "rentals_rental"
        verbose_name = _('Rental')
        verbose_name_plural = _('Rentals')
    
    def __repr__(self):
        username = self.student.username or self.student.email
        return f"<Rental: {username} -> Book: {self.book.title}>"