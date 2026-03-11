from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    MoodEntry, UserProfile, ChatMessage, ActivityLog, Feedback, AIAnalysis, AITransparency, DetectedPattern, FAQ, HowItWorksStep, AppConfig, Notification, Recommendation, PrivacyPolicy
)
from django.contrib.auth.models import User

class AppConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppConfig
        fields = '__all__'

class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        return data

class AIAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIAnalysis
        fields = '__all__'

class AITransparencySerializer(serializers.ModelSerializer):
    class Meta:
        model = AITransparency
        fields = '__all__'

class DetectedPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectedPattern
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'email', 'avatar_name', 'language', 'text_size', 
            'high_contrast', 'screen_reader', 'notifications_enabled', 'notification_time', 
            'mood_alerts_enabled', 'weekly_insights_enabled', 'emergency_alerts_enabled',
            'mental_health_score', 'age_range', 'bio', 'goals',
            'privacy_consent_accepted', 'essential_data_processing', 'anonymous_analytics', 'privacy_policy_version'
        ]

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    # Extra fields for profile creation
    privacy_consent_accepted = serializers.BooleanField(write_only=True, required=False)
    essential_data_processing = serializers.BooleanField(write_only=True, required=False)
    anonymous_analytics = serializers.BooleanField(write_only=True, required=False)
    privacy_policy_version = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'profile',
            'privacy_consent_accepted', 'essential_data_processing', 'anonymous_analytics', 'privacy_policy_version'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        # Extract profile-related fields
        privacy_data = {
            'privacy_consent_accepted': validated_data.pop('privacy_consent_accepted', False),
            'essential_data_processing': validated_data.pop('essential_data_processing', True),
            'anonymous_analytics': validated_data.pop('anonymous_analytics', False),
            'privacy_policy_version': validated_data.pop('privacy_policy_version', '1.0.0'),
        }

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Create or update profile with the privacy data
        profile, created = UserProfile.objects.get_or_create(user=user)
        for key, value in privacy_data.items():
            setattr(profile, key, value)
        profile.save()
        
        return user

from .utils import format_relative_time

class MoodEntrySerializer(serializers.ModelSerializer):
    formattedTime = serializers.SerializerMethodField(method_name='get_formatted_time')
    
    class Meta:
        model = MoodEntry
        fields = '__all__'
        read_only_fields = ['user']

    def get_formatted_time(self, obj):
        return format_relative_time(obj.timestampMillis)

    def create(self, validated_data):
        # Generate aiReflection if missing or empty
        if not validated_data.get('aiReflection'):
            # Create a temporary instance to call the generation logic 
            # or just use the logic directly on cleaned data
            mood = MoodEntry(**validated_data)
            validated_data['aiReflection'] = mood.generate_reflection()
        return super().create(validated_data)

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
        read_only_fields = ['user']

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = '__all__'
        read_only_fields = ['user']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['user']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class HowItWorksStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = HowItWorksStep
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['user']

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'
        read_only_fields = ['user']
