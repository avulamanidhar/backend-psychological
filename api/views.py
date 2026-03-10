from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import MoodEntry, UserProfile, ChatMessage, ActivityLog, Feedback
from .serializers import (
    MoodEntrySerializer, UserSerializer, UserProfileSerializer, 
    ChatMessageSerializer, ActivityLogSerializer, FeedbackSerializer
)
from django.contrib.auth.models import User
from django.db.models import Avg
import random

# ... (Previous views omit for brevity in target)

class FeedbackCreate(APIView):
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InsightDataView(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        # Mocking weekly data for 7 days
        mood_data = [0.4, 0.45, 0.5, 0.42, 0.6, 0.7, 0.65] 
        stress_data = [0.3, 0.35, 0.4, 0.38, 0.45, 0.5, 0.48]
        anxiety_data = [0.2, 0.25, 0.3, 0.28, 0.35, 0.4, 0.38]
        
        return Response({
            "mood_scores": mood_data,
            "stress_scores": stress_data,
            "anxiety_scores": anxiety_data,
            "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        })

class DetectedPatternsView(APIView):
    def get(self, request, username):
        patterns = [
            {
                "title": "Monday Anxiety",
                "description": "You tend to report higher anxiety on Monday mornings.",
                "confidence": "92%",
                "type": "negative"
            },
            {
                "title": "Post-Exercise Boost",
                "description": "Your mood improves by ~40% after physical activity.",
                "confidence": "88%",
                "type": "positive"
            },
            {
                "title": "Late Night Stress",
                "description": "Stress indicators rise after 10 PM on weekdays.",
                "confidence": "76%",
                "type": "warning"
            }
        ]
        return Response(patterns)

class HealthScoreDetail(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(UserProfile, user=user)
        
        # Calculate dynamic scores based on data
        mood_avg = MoodEntry.objects.filter(user=user).aggregate(Avg('intensity'))['intensity__avg'] or 75
        
        return Response({
            "main_score": profile.mental_health_score,
            "mood_score": int(mood_avg),
            "stress_score": 65,
            "sleep_score": 71,
            "social_score": 88
        })

class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileDetail(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(UserProfile, user=user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(UserProfile, user=user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MoodEntryList(APIView):
    def get(self, request):
        username = request.query_params.get('username')
        if username:
            moods = MoodEntry.objects.filter(user__username=username)
        else:
            moods = MoodEntry.objects.all()
        serializer = MoodEntrySerializer(moods, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MoodEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MoodEntryDetail(APIView):
    def get(self, request, pk):
        mood = get_object_or_404(MoodEntry, pk=pk)
        serializer = MoodEntrySerializer(mood)
        return Response(serializer.data)

    def put(self, request, pk):
        mood = get_object_or_404(MoodEntry, pk=pk)
        serializer = MoodEntrySerializer(mood, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        mood = get_object_or_404(MoodEntry, pk=pk)
        mood.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChatMessageList(APIView):
    def get(self, request):
        username = request.query_params.get('username')
        if username:
            messages = ChatMessage.objects.filter(user__username=username)
        else:
            messages = ChatMessage.objects.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Logic for AI Response could go here
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivityLogList(APIView):
    def get(self, request):
        username = request.query_params.get('username')
        if username:
            logs = ActivityLog.objects.filter(user__username=username)
        else:
            logs = ActivityLog.objects.all()
        serializer = ActivityLogSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ActivityLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardSummary(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(UserProfile, user=user)
        latest_mood = MoodEntry.objects.filter(user=user).first()
        avg_intensity = MoodEntry.objects.filter(user=user).aggregate(Avg('intensity'))['intensity__avg'] or 0
        
        # Simple Logic for Alert
        risk_level = "Low"
        if avg_intensity < 30:
            risk_level = "High"
        elif avg_intensity < 50:
            risk_level = "Moderate"

        recommendation = "Try a breathing exercise to stay grounded."
        if latest_mood and latest_mood.intensity < 40:
             recommendation = "You seem a bit low. Consider a meditation session."

        data = {
            "greeting": f"Hello, {user.username}!",
            "latest_mood": MoodEntrySerializer(latest_mood).data if latest_mood else None,
            "mental_health_score": profile.mental_health_score,
            "risk_level": risk_level,
            "recommended_activity": recommendation
        }
        return Response(data)
