
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


class RentalSerializer(serializers.ModelSerializer):
    book = BookBriefSerializer(read_only=True)  # Remove 'many=True'
    rental_duration = serializers.SerializerMethodField()
    pending_fee = serializers.SerializerMethodField()

    class Meta:
        model = Rental
        fields = ['id', 'book', 'rental_date', 'return_date', 'returned', 'rental_duration', 'pending_fee']

    def get_rental_duration(self, obj):
        return obj._rental_duration()

    def get_pending_fee(self, obj):
        return obj._rental_fee()


class StudentRentalSerializer(serializers.ModelSerializer):
    rentals = RentalSerializer(many=True, read_only=True)
    total_fee = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'rentals', 'total_fee']

    def get_total_fee(self, obj):
        return sum(rental._rental_fee() for rental in obj.rental_set.filter(returned=0))