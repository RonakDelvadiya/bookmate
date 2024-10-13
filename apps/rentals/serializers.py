
from rest_framework import serializers
from .models import Rental
from books.serializers import BookBriefSerializer, UserSerializer

from django.contrib.auth import get_user_model
User = get_user_model()

class RentalListSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    book = BookBriefSerializer(read_only=True)

    class Meta:
        model = Rental
        fields = ['id', 'student', 'book', 'rental_date', 'returned', '_rental_fee']


class RentalUpdateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['student', 'book', 'rental_date', 'return_date']
        extra_kwargs = {
            'student': {'required': True},
            'book': {'required': True},
            'rental_date': {'required': True},
            'return_date': {'required': False, 'allow_null': True}
        }