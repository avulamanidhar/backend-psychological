from django.urls import path
from .views import (
    UserList, 
    UserProfileDetail,
    MoodEntryList, 
    MoodEntryDetail,
    ChatMessageList,
    ActivityLogList,
    DashboardSummary,
    InsightDataView,
    DetectedPatternsView,
    HealthScoreDetail,
    FeedbackCreate,
    LoginView,
    ForgotPasswordView
)

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('profile/<str:username>/', UserProfileDetail.as_view(), name='user-profile'),
    path('moods/', MoodEntryList.as_view(), name='mood-list'),
    path('moods/<str:pk>/', MoodEntryDetail.as_view(), name='mood-detail'),
    path('chat/', ChatMessageList.as_view(), name='chat-list'),
    path('activities/', ActivityLogList.as_view(), name='activity-list'),
    path('dashboard/<str:username>/', DashboardSummary.as_view(), name='dashboard-summary'),
    path('insights/trends/<str:username>/', InsightDataView.as_view(), name='insight-trends'),
    path('insights/patterns/<str:username>/', DetectedPatternsView.as_view(), name='insight-patterns'),
    path('health-score/<str:username>/', HealthScoreDetail.as_view(), name='health-score-detail'),
    path('feedback/', FeedbackCreate.as_view(), name='feedback-create'),
]
