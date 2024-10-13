from django.urls import path
from .views import RentalRetrieveUpdateDestroyView, RentalListCreateView
from .admin import RentalAdmin


urlpatterns = [
    path('admin/rental/student-dashboard/', RentalAdmin.student_dashboard_view, name='admin_student_dashboard'),
    path('rental-list-create/', RentalListCreateView.as_view(), name='rental-list-create'),
    path('rental-action/<int:pk>/', RentalRetrieveUpdateDestroyView.as_view(), name='rental-detail'),
]
