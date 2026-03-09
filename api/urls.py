from django.urls import path
from .views import (
    UserList, 
    MoodEntryList, 
    MoodEntryDetail
)

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('moods/', MoodEntryList.as_view(), name='mood-list'),
    path('moods/<str:pk>/', MoodEntryDetail.as_view(), name='mood-detail'),
]
