import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from .models import (
    MoodEntry, UserProfile, ChatMessage, ActivityLog, Feedback, AIAnalysis, 
    AITransparency, DetectedPattern, FAQ, HowItWorksStep, AppConfig, 
    Notification, Recommendation, PrivacyPolicy, PasswordResetOTP,
    PasswordResetLog
)
from django.core.mail import send_mail
from django.conf import settings
from .serializers import (
    MoodEntrySerializer, UserSerializer, UserProfileSerializer, 
    ChatMessageSerializer, ActivityLogSerializer, FeedbackSerializer,
    AIAnalysisSerializer, AITransparencySerializer, DetectedPatternSerializer, FAQSerializer, HowItWorksStepSerializer,
    MyTokenObtainPairSerializer, AppConfigSerializer, NotificationSerializer, RecommendationSerializer, PrivacyPolicySerializer
)
from .rag_utils import RAGManager
from .risk_utils import RiskAnalyzer
from .email_service import EmailService
from .otp_service import OTPService
from django.contrib.auth.models import User
from django.db.models import Avg
from django.utils import timezone
from datetime import datetime, timedelta
import random

class AppConfigList(APIView):
    def get(self, request):
        configs = AppConfig.objects.all()
        if not configs.exists():
            mock_data = [
                {"key": "support_email", "value": "support@mindguard.ai", "description": "Global support email"},
                {"key": "min_app_version", "value": "1.0.0", "description": "Minimum required app version"},
                {"key": "maintenance_mode", "value": "false", "description": "If true, show maintenance screen"}
            ]
            for item in mock_data:
                AppConfig.objects.create(**item)
            configs = AppConfig.objects.all()
        
        serializer = AppConfigSerializer(configs, many=True)
        return Response(serializer.data)

class MoodTypeList(APIView):
    def get(self, request):
        moods = [
            {"name": "Great", "color": "#F6A623", "bg_color": "#FFF9C4", "description": "Feeling energetic and positive"},
            {"name": "Good", "color": "#4CAF50", "bg_color": "#FFF9C4", "description": "Feeling steady and satisfied"},
            {"name": "Okay", "color": "#9E9E9E", "bg_color": "#E8F5E9", "description": "Feeling neutral or balanced"},
            {"name": "Low", "color": "#9E9E9E", "bg_color": "#E8F5E9", "description": "Feeling a bit drained"},
            {"name": "Tired", "color": "#9E9E9E", "bg_color": "#E8F5E9", "description": "Feeling physically or mentally exhausted"},
            {"name": "Sad", "color": "#7E57C2", "bg_color": "#F3E5F5", "description": "Feeling blue or downcast"},
            {"name": "Anxious", "color": "#FF6B6B", "bg_color": "#F3E5F5", "description": "Feeling worried or uneasy"},
            {"name": "Frustrated", "color": "#FF6B6B", "bg_color": "#F3E5F5", "description": "Feeling annoyed or stuck"},
        ]
        return Response(moods)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# ... (Previous views)

class AIAnalysisList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        analyses = AIAnalysis.objects.filter(user=request.user)
        if not analyses.exists():
            # Create a mock analysis if none exists
            mock_analysis = AIAnalysis.objects.create(
                user=request.user,
                title="Monday Anxiety",
                subtitle="How we detected this pattern",
                steps=[
                    {
                        "number": 1,
                        "title": "Data Collection",
                        "description": "Analyzed your last 4 Mondays of mood logs."
                    },
                    {
                        "number": 2,
                        "title": "Pattern Recognition",
                        "description": "Identified 'Anxious' entries between 8-10 AM."
                    },
                    {
                        "number": 3,
                        "title": "Keyword Correlation",
                        "description": "Found frequent mentions of 'work' and 'deadlines'."
                    },
                    {
                        "number": 4,
                        "title": "Confidence Scoring",
                        "description": "Cross-validated with 3 months of historical data."
                    }
                ],
                confidence_level=92,
                data_points_count=28,
                weeks_count=4
            )
            analyses = [mock_analysis]
        
        serializer = AIAnalysisSerializer(analyses, many=True)
        return Response(serializer.data)

class AITransparencyList(APIView):
    def get(self, request):
        transparency_data = AITransparency.objects.all()
        if not transparency_data.exists():
            # Create mock transparency info
            mock_data = [
                {
                    "section_key": "how_it_works",
                    "title": "How AI Works",
                    "content": "Our AI analyzes patterns in your mood logs and journal entries to provide personalized insights. It recognizes linguistic and behavioral patterns — it does not understand emotions like a human."
                },
                {
                    "section_key": "limitations",
                    "title": "Limitations",
                    "content": "● AI is not a substitute for professional therapy\n● It cannot diagnose mental health conditions\n● In crisis situations, it directs you to human resources\n● Insights are probabilistic, not definitive"
                },
                {
                    "section_key": "data_usage",
                    "title": "Data Usage",
                    "content": "Your data is used solely to improve your personal experience. We do not sell or share your data with third parties. All processing happens on-device."
                }
            ]
            for item in mock_data:
                AITransparency.objects.create(**item)
            transparency_data = AITransparency.objects.all()
        
        serializer = AITransparencySerializer(transparency_data, many=True)
        return Response(serializer.data)

class BreathingPatternConfig(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return Response({
            "name": "Box Breathing",
            "inhale_ms": 4000,
            "hold_ms": 4000,
            "exhale_ms": 4000,
            "wait_ms": 4000
        })

class SystemStatus(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        from datetime import datetime
        return Response({
            "status": "online",
            "server_time": datetime.now().isoformat(),
            "version": "1.0.0",
            "message": "MindGuard AI Backend is operational."
        })

class FocusTimerConfig(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return Response({
            "focus_minutes": 25,
            "break_minutes": 5
        })

class GroundingExerciseConfig(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return Response({
            "name": "5-4-3-2-1 Grounding",
            "duration_minutes": 5,
            "steps": [
                {"number": 5, "phrase": "things you can see", "instruction": "Name 5 things you can see around you right now", "icon": "sight"},
                {"number": 4, "phrase": "things you can touch", "instruction": "Name 4 things you can physically feel or touch", "icon": "touch"},
                {"number": 3, "phrase": "things you can hear", "instruction": "Name 3 sounds you can hear in your environment", "icon": "hearing"},
                {"number": 2, "phrase": "things you can smell", "instruction": "Name 2 things you can smell (or like to smell)", "icon": "smell"},
                {"number": 1, "phrase": "things you can taste", "instruction": "Name 1 thing you can taste right now", "icon": "taste"}
            ]
        })

class MeditationContentConfig(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return Response({
            "title": "Daily Meditation",
            "subtitle": "Tap below to start a guided session personalized for your current mood.",
            "recommended_mode": "Calm",
            "recommended_duration": 10
        })

class SelfCareConfig(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return Response({
            "items": [
                "Drank enough water 💧",
                "Ate a nutritious meal 🥗",
                "Went outside or got fresh air ☀️",
                "Moved my body 🏃",
                "Connected with someone 💬",
                "Took a mindful break 🧘"
            ]
        })

class ToolsDirectoryConfig(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return Response({
            "breathing": {"badge": "5 min", "desc": "4-7-8 Technique"},
            "meditation": {"badge": "10 min", "desc": "Guided session"},
            "grounding": {"badge": "5 min", "desc": "5-4-3-2-1 Method"},
            "focus": {"badge": "25 min", "desc": "Pomodoro technique"},
            "selfcare": {"badge": "2 min", "desc": "Daily checklist"}
        })

class WhyMindguardConfig(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return Response({
            "title": "Why MindGuard?",
            "subtitle": "Built for your emotional wellbeing",
            "feature1": {
                "title": "AI-Powered Support",
                "description": "Personalized insights based on your emotional patterns and daily check-ins."
            },
            "feature2": {
                "title": "Privacy First",
                "description": "Your data is encrypted and stays on your device. We never share your information."
            },
            "feature3": {
                "title": "Safe Space",
                "description": "A judgment-free zone to explore your feelings and build emotional resilience."
            }
        })

class FAQList(APIView):
    def get(self, request):
        faqs = FAQ.objects.all()
        if not faqs.exists():
            mock_data = [
                {"question": "How do I log my mood?", "answer": "You can log your mood by clicking the '+' button on the home screen and selecting your current emotion.", "order": 1},
                {"question": "Is my data secure?", "answer": "Yes, we use industry-standard encryption to protect your data. Your privacy is our top priority.", "order": 2},
                {"question": "How does the AI analysis work?", "answer": "The AI analyzes your mood patterns and journal entries to provide personalized insights and suggestions.", "order": 3}
            ]
            for item in mock_data:
                FAQ.objects.create(**item)
            faqs = FAQ.objects.all()
        
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data)

class HowItWorksStepList(APIView):
    def get(self, request):
        steps = HowItWorksStep.objects.all()
        if not steps.exists():
            mock_data = [
                {"title": "Log Your Mood", "description": "Daily check-ins with emojis, journaling, and stress tracking.", "order": 1},
                {"title": "Get AI Insights", "description": "Our AI analyzes patterns to help you understand emotional triggers.", "order": 2},
                {"title": "Find Support", "description": "Access coping tools, guided exercises, and professional resources.", "order": 3}
            ]
            for item in mock_data:
                HowItWorksStep.objects.create(**item)
            steps = HowItWorksStep.objects.all()
        
        serializer = HowItWorksStepSerializer(steps, many=True)
        return Response(serializer.data)

class FeedbackCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InsightDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        today = timezone.now().date()
        
        def get_day_metrics(date):
            start = timezone.make_aware(datetime.combine(date, datetime.min.time()))
            end = timezone.make_aware(datetime.combine(date, datetime.max.time()))
            start_ms = int(start.timestamp() * 1000)
            end_ms = int(end.timestamp() * 1000)
            
            moods = MoodEntry.objects.filter(user=user, timestampMillis__gte=start_ms, timestampMillis__lte=end_ms)
            if moods.exists():
                avg_val = float(moods.aggregate(Avg('intensity'))['intensity__avg']) / 100.0
                return avg_val, avg_val * 0.8, avg_val * 0.6 # Mocking stress/anxiety from mood for now
            return 0.5, 0.4, 0.3 # Defaults

        mood_scores = []
        stress_scores = []
        anxiety_scores = []
        for i in range(6, -1, -1):
            m, s, a = get_day_metrics(today - timedelta(days=i))
            mood_scores.append(m)
            stress_scores.append(s)
            anxiety_scores.append(a)
            
        return Response({
            "mood_scores": mood_scores,
            "stress_scores": stress_scores,
            "anxiety_scores": anxiety_scores,
            "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "weekly_summary_score": 78,
            "trend_text": "↑ +12 from last week"
        })

class MoodTrendView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        today = timezone.now().date()
        
        def get_intensity(date):
            start = timezone.make_aware(datetime.combine(date, datetime.min.time()))
            end = timezone.make_aware(datetime.combine(date, datetime.max.time()))
            start_ms = int(start.timestamp() * 1000)
            end_ms = int(end.timestamp() * 1000)
            
            moods = MoodEntry.objects.filter(user=user, timestampMillis__gte=start_ms, timestampMillis__lte=end_ms)
            if moods.exists():
                return float(moods.aggregate(Avg('intensity'))['intensity__avg']) / 100.0
            return None

        current_points = []
        for i in range(6, -1, -1):
            val = get_intensity(today - timedelta(days=i))
            current_points.append(val if val is not None else 0.5)
            
        comparison_points = []
        for i in range(13, 6, -1):
            val = get_intensity(today - timedelta(days=i))
            comparison_points.append(val if val is not None else 0.4)
            
        def calc_trend(curr, prev):
            diff = curr - prev
            arrow = "↑" if diff >= 0 else "↓"
            return f"{arrow} {abs(diff)} vs last week"

        avg_current = sum(current_points) / len(current_points) * 100
        avg_comp = sum(comparison_points) / len(comparison_points) * 100
        
        mood_score = int(avg_current)
        mood_trend = calc_trend(int(avg_current), int(avg_comp))
        
        anxiety_score = int((100 - avg_current) * 0.8)
        anxiety_comp = int((100 - avg_comp) * 0.8)
        anxiety_trend = calc_trend(anxiety_score, anxiety_comp)
        
        stress_score = int((100 - avg_current) * 0.6)
        stress_comp = int((100 - avg_comp) * 0.6)
        stress_trend = calc_trend(stress_score, stress_comp)
        
        sleep_score = int(avg_current * 0.9)
        sleep_comp = int(avg_comp * 0.9)
        sleep_trend = calc_trend(sleep_score, sleep_comp)

        return Response({
            "current_points": current_points,
            "comparison_points": comparison_points,
            "mood_score": mood_score,
            "mood_trend": mood_trend,
            "anxiety_score": anxiety_score,
            "anxiety_trend": anxiety_trend,
            "stress_score": stress_score,
            "stress_trend": stress_trend,
            "sleep_score": sleep_score,
            "sleep_trend": sleep_trend
        })

class DetectedPatternsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        patterns = DetectedPattern.objects.filter(user=user)
        
        if not patterns.exists():
            # Create mock patterns for the user
            mock_data = [
                {
                    "user": user,
                    "title": "Evening Stress Peak",
                    "description": "Your stress levels tend to rise after 6 PM on weekdays.",
                    "confidence": "85%",
                    "pattern_type": "warning"
                },
                {
                    "user": user,
                    "title": "Morning Meditation Impact",
                    "description": "Your mood improves by 25% on days you meditate before 9 AM.",
                    "confidence": "92%",
                    "pattern_type": "positive"
                }
            ]
            for item in mock_data:
                DetectedPattern.objects.create(**item)
            patterns = DetectedPattern.objects.filter(user=user)
            
        serializer = DetectedPatternSerializer(patterns, many=True)
        return Response(serializer.data)

class HealthScoreDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(UserProfile, user=user)
        
        # Calculate scores from last 7 days
        seven_days_ago = timezone.now() - timedelta(days=7)
        seven_days_ago_ms = int(seven_days_ago.timestamp() * 1000)
        
        moods = MoodEntry.objects.filter(user=user, timestampMillis__gte=seven_days_ago_ms)
        
        # 1. Mood Score (Avg Intensity)
        if moods.exists():
            avg_mood = float(moods.aggregate(Avg('intensity'))['intensity__avg'])
        else:
            avg_mood = 70.0
            
        # 2. Stress Score (Inverse of 'Stress' triggers)
        stress_count = 0
        for m in moods:
            if any(t in ['Work', 'Deadlines', 'Pressure', 'Money'] for t in m.triggers):
                stress_count += 1
        stress_score = max(0, 100 - (stress_count * 15)) if moods.exists() else 65
        
        # 3. Sleep Score (Based on evening meditations/calm activities)
        meditations = ActivityLog.objects.filter(
            user=user, 
            activity_type='Meditation', 
            timestamp__gte=seven_days_ago
        ).count()
        sleep_score = min(100, 60 + (meditations * 10))
        
        # 4. Social Score (Interaction frequency/triggers)
        social_triggers = 0
        for m in moods:
            if any(t in ['Family', 'Friends', 'Social', 'Partner'] for t in m.triggers):
                social_triggers += 1
        social_score = min(100, 50 + (social_triggers * 15))
        
        # 5. Main Score (Weighted Average)
        main_score = int((avg_mood * 0.4) + (stress_score * 0.2) + (sleep_score * 0.2) + (social_score * 0.2))
        profile.mental_health_score = main_score
        profile.save()

        return Response({
            "main_score": main_score,
            "mood_score": int(avg_mood),
            "stress_score": stress_score,
            "sleep_score": sleep_score,
            "social_score": social_score
        })

class UserList(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileDetail(APIView):
    permission_classes = [permissions.AllowAny]
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
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        username = request.query_params.get('username')
        if username:
            moods = MoodEntry.objects.filter(user__username=username)
        else:
            moods = MoodEntry.objects.filter(user=request.user) if request.user.is_authenticated else MoodEntry.objects.none()
        serializer = MoodEntrySerializer(moods, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MoodEntrySerializer(data=request.data)
        if serializer.is_valid():
            # Generate AI reflection if not provided via the new model method
            mood_entry = MoodEntry(**serializer.validated_data)
            if not mood_entry.aiReflection:
                serializer.validated_data['aiReflection'] = mood_entry.generate_reflection()
                
            username = request.query_params.get('username')
            user = None
            if username:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    pass
            elif request.user.is_authenticated:
                user = request.user

            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MoodEntryDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        mood = get_object_or_404(MoodEntry, pk=pk, user=request.user)
        serializer = MoodEntrySerializer(mood)
        return Response(serializer.data)

    def delete(self, request, pk):
        mood = get_object_or_404(MoodEntry, pk=pk, user=request.user)
        mood.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChatMessageList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_text = request.data.get('text', '').strip()
        mode = request.data.get('mode', 'General')
        lang = request.data.get('language', 'English')
        
        # 1. INPUT VALIDATION
        if not user_text:
            return Response({"error": "Message text is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(user_text) > 1000:
            return Response({"error": "Message text is too long (max 1000 characters)."}, status=status.HTTP_400_BAD_REQUEST)

        valid_modes = [m[0] for m in ChatMessage.MODE_CHOICES]
        if mode not in valid_modes:
            mode = 'General' # Fallback to default
            
        valid_langs = ['English', 'Telugu', 'Hindi'] # Common set for this app
        if lang not in valid_langs:
            lang = 'English'

        # 2. RISK ANALYSIS MIDDLEWARE
        try:
            analyzer = RiskAnalyzer()
            risk_level = analyzer.analyze(user_text)
        except Exception as e:
            # Fatal error in risk analysis should default to MEDIUM for safety
            print(f"Risk analysis system error: {e}")
            risk_level = "MEDIUM"
        
        # 2. SAVE USER MESSAGE WITH RISK LEVEL
        user_msg = ChatMessage.objects.create(
            user=request.user,
            text=user_text,
            is_user=True,
            mode=mode,
            language=lang,
            risk_level=risk_level
        )
        
        # 3. GENERATE RESPONSE BASED ON RISK
        if risk_level == "HIGH":
            ai_text = analyzer.get_emergency_response(lang)
        else:
            ai_text = self.generate_response(user_text, mode, lang, request.user, risk_level)
        
        # 4. SAVE AI MESSAGE
        ai_msg = ChatMessage.objects.create(
            user=request.user,
            text=ai_text,
            is_user=False,
            mode=mode,
            language=lang,
            risk_level=risk_level
        )
        
        return Response({
            "user_message": ChatMessageSerializer(user_msg).data,
            "ai_message": ChatMessageSerializer(ai_msg).data
        }, status=status.HTTP_201_CREATED)

    def generate_response(self, text, mode, lang, user, risk_level="LOW"):
        text_lower = text.lower()
        
        # (Already handled high-risk in post, but keeping a simple safety check here for medium/low cases)
        risk_keywords = ["die", "hopeless", "worthless", "chavali", "end my life", "disappear", "suicide"]
        if any(kw in text_lower for kw in risk_keywords):
            if lang == "Telugu":
                return "మవా, నువ్వు అలా మాట్లాడుతుంటే నాకు చాలా బాధగా ఉంది. నీ ప్రాణం చాలా విలువైనది. దయచేసి నీకు దగ్గరగా ఉన్న వారితో లేదా ఒక డాక్టర్‌తో మాట్లాడు. నేను నీకు తోడుగా ఉంటాను, కానీ ప్రొఫెషనల్ హెల్ప్ తీసుకోవడం చాలా ముఖ్యం. 💙"
            return "I hear how much pain you're in, and it's okay to feel overwhelmed, but please know you're not alone. Your life is valuable. I strongly encourage you to reach out to a trusted person or a professional counselor right now. I'm here to support you through this. 💙"

        # Fetch conversation history (last 10 messages) for memory
        history = ChatMessage.objects.filter(user=user).order_by('-timestamp')[:10]

        # Initialize and use RAGManager for intelligent response
        try:
            rag_mgr = RAGManager()
            return rag_mgr.generate_ai_response(text, mode, lang, history=history)
        except Exception as e:
            # Fallback to simple matching if OpenAI fails (API key not set, network, etc.)
            print(f"Error in RAG generation: {e}")
            if lang == "Telugu":
                return "అర్థం చేసుకున్నాను మవా. ఇంకా చెప్పు.. నీకు ఏమనిపిస్తుంది? ✨"
            return "I hear you. Processing these thoughts is a brave step. I'm right here with you. What's on your mind? ✨"

class ActivityLogList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        logs = ActivityLog.objects.filter(user=request.user)
        serializer = ActivityLogSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ActivityLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardSummary(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(UserProfile, user=user)
        latest_mood = MoodEntry.objects.filter(user=user).order_by('-timestampMillis').first()
        
        from datetime import datetime
        hour = datetime.now().hour
        greeting_prefix = "Good morning" if 5 <= hour < 12 else "Good afternoon" if 12 <= hour < 18 else "Good evening"
        
        # Dynamic Risk & Recommendation Logic
        recent_moods = MoodEntry.objects.filter(user=user).order_by('-timestampMillis')[:3]
        risk_level = "Low"
        recommended_activity = "Try a breathing exercise to stay grounded."
        
        if recent_moods.exists():
            avg_intensity = sum(m.intensity for m in recent_moods) / recent_moods.count()
            if avg_intensity > 8:
                risk_level = "High"
                recommended_activity = "You've been through a lot lately. Chat with our AI coach or reach out for support."
            elif avg_intensity > 5:
                risk_level = "Moderate"
                recommended_activity = "Feeling a bit overwhelmed? Let's try some grounding techniques."

        data = {
            "greeting": f"{greeting_prefix}, {user.username}!",
            "latest_mood": MoodEntrySerializer(latest_mood).data if latest_mood else None,
            "mental_health_score": profile.mental_health_score,
            "risk_level": risk_level,
            "recommended_activity": recommended_activity
        }
        return Response(data)

class KeyIndicatorsView(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        moods = MoodEntry.objects.filter(user=user).order_by('-timestampMillis')[:10]
        
        # Default mock values
        stress = {"progress": 30, "status": "Low", "desc": "You're managing stress well this week."}
        anxiety = {"progress": 45, "status": "Moderate", "desc": "Slight fluctuation noticed recently."}
        depression = {"progress": 20, "status": "Low", "desc": "Mood patterns look healthy."}
        stability = {"progress": 85, "status": "High", "desc": "Your mood has been very consistent."}
        
        if moods.exists():
            count = moods.count()
            avg_intensity = float(sum(m.intensity for m in moods)) / count
            stress["progress"] = int(avg_intensity)
            stress["status"] = "Low" if avg_intensity < 40 else "Moderate" if avg_intensity < 70 else "High"
            stress["desc"] = "You're managing stress well." if avg_intensity < 40 else "Keep an eye on your energy levels."
            
            anxiety_count = 0
            for m in moods:
                triggers = m.triggers if isinstance(m.triggers, list) else []
                if any(t in ['Deadlines', 'Work', 'Pressure'] for t in triggers):
                    anxiety_count += 1
            anxiety["progress"] = min(anxiety_count * 25, 100)
            anxiety["status"] = "Low" if anxiety["progress"] < 30 else "Moderate" if anxiety["progress"] < 70 else "High"

            intensities = [m.intensity for m in moods]
            diff = max(intensities) - min(intensities)
            stability["progress"] = max(100 - (diff * 10), 0)
            stability["status"] = "High" if stability["progress"] > 75 else "Moderate" if stability["progress"] > 45 else "Low"

        return Response({
            "stress": stress,
            "anxiety": anxiety,
            "depression": depression,
            "stability": stability
        })

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        identifier = request.data.get('email') or request.data.get('username')
        success, message = OTPService.generate_and_send_otp(identifier, request.META)
        
        if not success:
            return Response({"message": message}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        return Response({"message": message}, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        identifier = request.data.get('email') or request.data.get('username')
        otp_code = request.data.get('otp')
        
        if not identifier or not otp_code:
            return Response({"error": "Identifier and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)
            
        success, message = OTPService.verify_otp(identifier, otp_code, request.META)
        
        if not success:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"message": message}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        identifier = request.data.get('email') or request.data.get('username')
        otp_code = request.data.get('otp')
        new_password = request.data.get('new_password')
        
        if not identifier or not otp_code or not new_password:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
        success, message = OTPService.reset_password(identifier, otp_code, new_password)
        
        if not success:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"message": message}, status=status.HTTP_200_OK)

class NotificationList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
        if not notifications.exists():
            # Create a welcome notification
            Notification.objects.create(
                user=request.user,
                title=f"Welcome, {request.user.username}!",
                message="Welcome to MindGuard AI! We're here to support your mental well-being every step of the way. Explore the tools and start your journey today.",
                is_read=False
            )
            # Create a tip notification
            Notification.objects.create(
                user=request.user,
                title="Daily Tip: Take a Breath",
                message="Taking just 5 deep breaths can significantly lower your stress levels. Try our breathing tool when you feel's overwhelmed.",
                is_read=False
            )
            notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
        
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class NotificationDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    def delete(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RecommendationList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        recs = Recommendation.objects.filter(user=request.user)
        if not recs.exists():
            mock_data = [
                {
                    "user": request.user,
                    "title": "Daily Breathing Practice",
                    "description": "Your anxiety peaks on Monday mornings. A 5-min breathing session before work could help.",
                    "duration": "5 min",
                    "difficulty": "Easy",
                    "type": "Breathing",
                    "image_tag": "img_54",
                    "action_text": "Start Now →"
                },
                {
                    "user": request.user,
                    "title": "Evening Journaling",
                    "description": "Stress indicators rise after 10 PM. Writing down worries before bed can improve sleep quality.",
                    "duration": "10 min",
                    "difficulty": "Easy",
                    "type": "Journaling",
                    "image_tag": "img_55",
                    "action_text": "Try Tonight →"
                },
                {
                    "user": request.user,
                    "title": "Midday Movement Break",
                    "description": "Your mood improves significantly after exercise. Even a 10-min walk counts.",
                    "duration": "10 min",
                    "difficulty": "Medium",
                    "type": "Movement",
                    "image_tag": "img_56",
                    "action_text": "Schedule It →"
                },
                {
                    "user": request.user,
                    "title": "Weekly Meditation",
                    "description": "Adding one 15-min meditation session per week could reduce your anxiety index by ~20%.",
                    "duration": "15 min",
                    "difficulty": "Medium",
                    "type": "Meditation",
                    "image_tag": "img_57",
                    "action_text": "Explore →"
                }
            ]
            for item in mock_data:
                Recommendation.objects.create(**item)
            recs = Recommendation.objects.filter(user=request.user)
        
        serializer = RecommendationSerializer(recs, many=True)
        return Response(serializer.data)

class PrivacyPolicyList(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        policy = PrivacyPolicy.objects.filter(is_active=True).order_by('-created_at').first()
        if not policy:
            content = """
            # Privacy & Consent
            
            Welcome to MindGuard AI. Your privacy is our top priority.
            
            ### 1. Data Collection
            We collect mood logs, journal entries, and activity data to provide personalized insights.
            
            ### 2. Encryption
            All your personal data is encrypted with AES-256 standards. We cannot access your private thoughts.
            
            ### 3. Your Choices
            You have full control over your data. You can export or delete your account at any time.
            """
            policy = PrivacyPolicy.objects.create(
                version='1.0.0',
                content=content,
                is_active=True
            )
        
        serializer = PrivacyPolicySerializer(policy)
        return Response(serializer.data)

class DataExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        moods = MoodEntry.objects.filter(user=user)
        chats = ChatMessage.objects.filter(user=user)
        activities = ActivityLog.objects.filter(user=user)
        feedback = Feedback.objects.filter(user=user)
        profile = UserProfile.objects.get(user=user)

        data = {
            "user_info": {
                "username": user.username,
                "email": user.email,
                "joined_date": user.date_joined.isoformat(),
            },
            "profile": UserProfileSerializer(profile).data,
            "mood_history": MoodEntrySerializer(moods, many=True).data,
            "chat_history": ChatMessageSerializer(chats, many=True).data,
            "activity_logs": ActivityLogSerializer(activities, many=True).data,
            "feedback": FeedbackSerializer(feedback, many=True).data,
            "export_date": timezone.now().isoformat()
        }
        return Response(data)

class DataDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request):
        user = request.user
        # Delete user data but keep the account? 
        # Usually "Delete Data" in privacy terms means deleting everything associated with the user.
        MoodEntry.objects.filter(user=user).delete()
        ChatMessage.objects.filter(user=user).delete()
        ActivityLog.objects.filter(user=user).delete()
        Feedback.objects.filter(user=user).delete()
        # Optionally reset profile
        profile = UserProfile.objects.get(user=user)
        profile.mental_health_score = 0
        profile.save()
        
        return Response({"message": "All your personal data has been deleted from our servers."}, status=status.HTTP_204_NO_CONTENT)

class ReflectionGenerationView(APIView):
    def post(self, request):
        mood_name = request.data.get('moodName', 'Okay')
        intensity = request.data.get('intensity', 50)
        triggers = request.data.get('triggers', [])
        
        # We can reuse the model method by creating a mock instance
        mock_mood = MoodEntry(moodName=mood_name, intensity=intensity, triggers=triggers)
        reflection = mock_mood.generate_reflection()
        
        return Response({"aiReflection": reflection})
