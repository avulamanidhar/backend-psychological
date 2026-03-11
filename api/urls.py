from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from .views import (
    UserList, 
    UserProfileDetail,
    MyTokenObtainPairView,
    MoodEntryList, 
    MoodEntryDetail,
    ChatMessageList,
    ActivityLogList,
    BreathingPatternConfig,
    FocusTimerConfig,
    GroundingExerciseConfig,
    MeditationContentConfig,
    SelfCareConfig,
    ToolsDirectoryConfig,
    WhyMindguardConfig,
    DashboardSummary,
    KeyIndicatorsView,
    InsightDataView,
    MoodTrendView,
    DetectedPatternsView,
    HealthScoreDetail,
    FeedbackCreate,
    ForgotPasswordView,
    AIAnalysisList,
    AITransparencyList,
    FAQList,
    SystemStatus,
    AppConfigList,
    HowItWorksStepList,
    MoodTypeList,
    NotificationList,
    NotificationDetail,
    RecommendationList,
    PrivacyPolicyList,
    DataExportView,
    DataDeleteView,
    ReflectionGenerationView
)

urlpatterns = [
    # Auth
    path('users/', UserList.as_view(), name='user-list'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    
    # Profile
    path('profile/<str:username>/', UserProfileDetail.as_view(), name='user-profile'),
    
    # Tracking
    path('moods/', MoodEntryList.as_view(), name='mood-list'),
    path('moods/<str:pk>/', MoodEntryDetail.as_view(), name='mood-detail'),
    path('chat/', ChatMessageList.as_view(), name='chat-list'),
    path('activities/', ActivityLogList.as_view(), name='activity-list'),
    path('activities/breathing-pattern/', BreathingPatternConfig.as_view(), name='breathing-pattern'),
    path('activities/focus-timer-config/', FocusTimerConfig.as_view(), name='focus-timer-config'),
    path('activities/grounding-exercise/', GroundingExerciseConfig.as_view(), name='grounding-exercise'),
    path('activities/meditation-content/', MeditationContentConfig.as_view(), name='meditation-content'),
    path('activities/self-care-config/', SelfCareConfig.as_view(), name='self-care-config'),
    path('activities/tools-directory/', ToolsDirectoryConfig.as_view(), name='tools-directory'),
    path('config/why-mindguard/', WhyMindguardConfig.as_view(), name='why-mindguard-config'),
    
    # Dashboard & Insights
    path('dashboard/<str:username>/', DashboardSummary.as_view(), name='dashboard-summary'),
    path('key-indicators/<str:username>/', KeyIndicatorsView.as_view(), name='key-indicators'),
    path('insights/trends/<str:username>/', InsightDataView.as_view(), name='insight-trends'),
    path('insights/graph/<str:username>/', MoodTrendView.as_view(), name='insight-graph'),
    path('insights/patterns/<str:username>/', DetectedPatternsView.as_view(), name='insight-patterns'),
    path('insights/analysis/', AIAnalysisList.as_view(), name='insight-analysis'),
    path('insights/transparency/', AITransparencyList.as_view(), name='insight-transparency'),
    path('health-score/<str:username>/', HealthScoreDetail.as_view(), name='health-score-detail'),
    
    # Other
    path('feedback/', FeedbackCreate.as_view(), name='feedback-create'),
    path('faq/', FAQList.as_view(), name='faq-list'),
    path('system/status/', SystemStatus.as_view(), name='system-status'),
    path('system/config/', AppConfigList.as_view(), name='app-config'),
    path('how-it-works/', HowItWorksStepList.as_view(), name='how-it-works-list'),
    path('system/moods/', MoodTypeList.as_view(), name='mood-types-list'),
    path('notifications/', NotificationList.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', NotificationDetail.as_view(), name='notification-detail'),
    path('recommendations/', RecommendationList.as_view(), name='recommendation-list'),
    path('privacy-policy/', PrivacyPolicyList.as_view(), name='privacy-policy-list'),
    path('user/export/', DataExportView.as_view(), name='data-export'),
    path('user/delete-data/', DataDeleteView.as_view(), name='data-delete'),
    path('reflection-generator/', ReflectionGenerationView.as_view(), name='reflection-generator'),
    
    # Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
