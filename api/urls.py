from django.urls import path, include
from rest_framework import routers
from .views import RatingViewSet, BookViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('books', BookViewSet)
router.register('ratings', RatingViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
