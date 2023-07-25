from django.urls import path, include
from rest_framework import routers
from .views import RatingViewSet, BookViewSet, UserViewSet
from rest_framework.authtoken.views import obtain_auth_token 
router = routers.DefaultRouter()
router.register('books', BookViewSet)
router.register('ratings', RatingViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('getUserToken/', obtain_auth_token)
]
