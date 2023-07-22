from django.shortcuts import render
from .serializers import BookSerializer, RatingSerializer, UserSerializer
from rest_framework import viewsets
from .models import Book, Rating
from django.contrib.auth.models import User

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

