from rest_framework import serializers
from .models import Book
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", 'first_name', 'last_name']

class BookListSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    last_modified_by = UserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'number_of_pages', 'created_by', 'last_modified_by', 'created_at', 'last_modified_at']
        read_only_fields = fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.created_by:
            representation['created_by'] = UserSerializer(instance.created_by).data
        if instance.last_modified_by:
            representation['last_modified_by'] = UserSerializer(instance.last_modified_by).data
        return representation


class BookBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'number_of_pages']
        read_only_fields = fields