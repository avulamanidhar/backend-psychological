from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MoodEntryViewSet, UserViewSet

router = DefaultRouter()
router.register(r'moods', MoodEntryViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
