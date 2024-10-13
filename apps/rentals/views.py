from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .models import Rental
from .serializers import RentalUpdateCreateSerializer, RentalListSerializer


class RentalListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Rental.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RentalListSerializer
        return RentalUpdateCreateSerializer

    def handle_exception(self, exc):
        if isinstance(exc, ObjectDoesNotExist):
            return Response({'error': 'Rental not found'}, status=status.HTTP_404_NOT_FOUND)
        elif isinstance(exc, IntegrityError) or isinstance(exc, ValidationError):
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            student = serializer.validated_data['student']
            book = serializer.validated_data['book']
            
            if Rental.objects.filter(student=student, book=book, returned=False).exists():
                error_str = "You have already rented this book."
                return self.handle_exception(ValidationError(error_str))
            
            serializer.save(created_by=self.request.user)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            return self.handle_exception(e)
        except Exception as e:
            return self.handle_exception(e)


class RentalRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Rental.objects.all()
    serializer_class = RentalUpdateCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RentalListSerializer
        return RentalUpdateCreateSerializer

    def handle_exception(self, exc):
        if isinstance(exc, ObjectDoesNotExist):
            return Response({'error': 'Rental not found'}, status=status.HTTP_404_NOT_FOUND)
        elif isinstance(exc, IntegrityError) or isinstance(exc, ValidationError):
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as exc:
            return self.handle_exception(exc)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(modified_by=self.request.user)
            return Response(serializer.data)
        except Exception as exc:
            return self.handle_exception(exc)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'success': 'Rental deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as exc:
            return self.handle_exception(exc)