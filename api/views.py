from django.shortcuts import render
from rest_framework.response import Response
from .serializers import BookSerializer, RatingSerializer, UserSerializer
from rest_framework import viewsets, status, request as req
from .models import Book, Rating
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {
                'message':'That is not the right way to perform this action!'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    @action(detail=True, methods=['delete'],  permission_classes=(IsAdminUser, ))
    def delete_book(self, request, pk=None,):
        book = Book.objects.get(id=pk)
        book.delete()
        return Response({
            'message':'Book deleted'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def rate_book(self, request, pk=None):
        if 'stars' in request.data:
            username = request.data['username']
            user = request.user
            book = Book.objects.get(id=pk)
            conf_user = User.objects.get(username=username)
            if(user != conf_user):
                return Response({
                    'message': "You can't Update Another person's rate!"
                })
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
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def update(self, request, *args, **kwargs):
        return Response({
            'message': 'Not the correct way to access update method.'
        }, status=status.HTTP_400_BAD_REQUEST)
    def create(self, request, *args, **kwargs):
        return Response({
            'message': 'Not the correct way to access create method.'
        }, status=status.HTTP_400_BAD_REQUEST)
        

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, create = Token.objects.get_or_create(user=serializer.instance)
        return Response({
            'Token': token.key,
        }, status=status.HTTP_201_CREATED)
    
    def list(self, request, *agrs, **kwargs):
        return Response(
            {
                "message":"You can't Access This function"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    def destroy(self, request, pk=None,*args, **kwargs):
        user = User.objects.get(id=pk)
        print(user)
        print(request.user)
        if user != request.user:
            return Response({
                'message':'Invalid action!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            user = request.user
            user.delete()
            return Response({
                'message':'User Deleted'
            }, status=status.HTTP_200_OK)
