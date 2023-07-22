from django.shortcuts import render
from rest_framework.response import Response
from .serializers import BookSerializer, RatingSerializer, UserSerializer
from rest_framework import viewsets, status, request as req
from .models import Book, Rating
from django.contrib.auth.models import User
from rest_framework.decorators import action

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['post'])
    def rate_book(self, request, pk=None):
        if 'stars' in request.data:
            username = request.data['username']
            book = Book.objects.get(id=pk)
            user = User.objects.get(username=username)
            try:
                # Check update first
                rating = Rating.objects.get(book=book, user=user)
                rating.stars = request.data['stars']
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                json = {
                    'message': 'Rating updated.',
                    'response': serializer.data
                }
                return Response(json, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(book=book, user=user, stars=request.data['stars'])
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                json = {
                    'message': 'Rating created.',
                    'response': serializer.data
                }
                return Response(json, status=status.HTTP_201_CREATED)
        else:
            print(request.data)
            json = {
                'message': 'stars not provided'
            }
            return Response(json , status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

