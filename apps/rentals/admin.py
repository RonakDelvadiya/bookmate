from django.utils.html import format_html
from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import Rental
from .serializers import StudentRentalSerializer
from django.db.models import Prefetch
from django.contrib.auth import get_user_model
User = get_user_model()


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['student', 'get_book_link', 'rental_date', 'return_date', 'returned', 'get_rental_duration', 'get_rental_fee']
    search_fields = ['student__username', 'student__email', 'book__title']
    list_filter = ['rental_date', 'returned']
    readonly_fields = ['get_rental_duration', 'get_rental_fee']
    change_list_template = 'admin/rental_changelist.html'

    def get_book_link(self, obj):
        url = reverse("admin:books_book_change", args=[obj.book.id])
        return format_html('<a href="{}">{}: {} pages</a>', 
                            url, 
                            obj.book.title, 
                            obj.book.number_of_pages)
    get_book_link.short_description = 'Book (Title: Pages)'
    get_book_link.admin_order_field = 'book__title'  # Allows column ordering

    def get_rental_duration(self, obj):
        try:
            return f"{obj._rental_duration()} days"
        except ValueError as e:
            return str(e)
    get_rental_duration.short_description = 'Rental Duration'

    def get_rental_fee(self, obj):
        try:
            return f"${obj._rental_fee():.2f}"
        except (ValueError, Rental.book.RelatedObjectDoesNotExist) as e:
            return str(e)
    get_rental_fee.short_description = 'Rental Fee'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('student', 'book')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('student_dashboard/', self.admin_site.admin_view(self.student_dashboard_view), name='rental_student_dashboard'),
        ]
        return custom_urls + urls


    @method_decorator(staff_member_required)
    def student_dashboard_view(self, request):
        context = dict(
            self.admin_site.each_context(request),
            title="Student Rental Dashboard"
        )

        students = User.objects.prefetch_related(
            Prefetch('rental_set', 
                     queryset=Rental.objects.filter(returned=False).select_related('book'),
                     to_attr='rentals'
                    )
        )
        serializer = StudentRentalSerializer(students, many=True)
        context['student_rentals'] = serializer.data
        return render(request, 'admin/student_dashboard.html', context)