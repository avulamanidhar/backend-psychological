from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar_name = models.CharField(max_length=100, default='default_avatar')
    language = models.CharField(max_length=20, default='English')
    text_size = models.CharField(max_length=20, default='Medium')
    high_contrast = models.BooleanField(default=False)
    screen_reader = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=True)
    notification_time = models.CharField(max_length=20, default="9:00 AM")
    mood_alerts_enabled = models.BooleanField(default=True)
    weekly_insights_enabled = models.BooleanField(default=False)
    emergency_alerts_enabled = models.BooleanField(default=True)
    mental_health_score = models.IntegerField(default=0)
    age_range = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    goals = models.JSONField(default=list, blank=True)
    
    # Privacy Consent Fields
    privacy_consent_accepted = models.BooleanField(default=False)
    essential_data_processing = models.BooleanField(default=True)
    anonymous_analytics = models.BooleanField(default=False)
    privacy_policy_version = models.CharField(max_length=20, default='1.0.0')

    def __str__(self):
        return f"Profile for {self.user.username}"

class PrivacyPolicy(models.Model):
    version = models.CharField(max_length=20, unique=True)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Privacy Policy v{self.version}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    rating = models.IntegerField(default=5)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} - {self.subject}"

class MoodEntry(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timestampMillis = models.BigIntegerField()
    moodName = models.CharField(max_length=50)
    moodImageResId = models.IntegerField()
    intensity = models.IntegerField()
    triggers = models.JSONField(default=list)
    journal = models.TextField(blank=True, null=True)
    aiReflection = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.moodName} ({self.intensity}) - {self.timestampMillis}"

    def generate_reflection(self):
        intensity_label = "low"
        if self.intensity >= 70:
            intensity_label = "high"
        elif self.intensity >= 30:
            intensity_label = "moderate"
            
        reflection = f"Based on this entry, you were experiencing {self.moodName.lower()} emotions with {intensity_label} intensity."
        
        if not self.triggers:
            reflection += " No specific triggers were identified."
        elif len(self.triggers) == 1:
            reflection += f" {self.triggers[0]} appear to be contributing factors."
        else:
            triggers_str = ""
            for i, t in enumerate(self.triggers):
                if i == 0:
                    triggers_str += t
                elif i == len(self.triggers) - 1:
                    triggers_str += f" and {t}"
                else:
                    triggers_str += f", {t}"
            reflection += f" {triggers_str} appear to be contributing factors."
        
        return reflection

    class Meta:
        ordering = ['-timestampMillis']

class ChatMessage(models.Model):
    MODE_CHOICES = [
        ('Calm', 'Calm'),
        ('CBT', 'CBT Coach'),
        ('Listener', 'Listener'),
        ('General', 'General'),
    ]
    RISK_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    text = models.TextField()
    is_user = models.BooleanField(default=True)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='General')
    language = models.CharField(max_length=20, default='English')
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES, default='LOW')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'User' if self.is_user else 'AI'} ({self.mode}): {self.text[:20]}..."

class ActivityLog(models.Model):
    ACTIVITY_TYPES = [
        ('Breathing', 'Breathing Exercise'),
        ('Grounding', 'Grounding Exercise'),
        ('Meditation', 'Meditation Session'),
        ('Focus', 'Focus Timer'),
        ('SelfCare', 'Self-Care Checklist'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    duration_minutes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict, blank=True)

class AIAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_analyses')
    title = models.CharField(max_length=100, default="AI Analysis")
    subtitle = models.CharField(max_length=200, default="How we detected this pattern")
    steps = models.JSONField(default=list) # List of { "number": 1, "title": "...", "description": "..." }
    confidence_level = models.IntegerField(default=0)
    data_points_count = models.IntegerField(default=0)
    weeks_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis: {self.title} for {self.user.username}"

class AITransparency(models.Model):
    section_key = models.CharField(max_length=50, unique=True) # e.g., 'how_it_works', 'limitations'
    title = models.CharField(max_length=255)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

class DetectedPattern(models.Model):
    PATTERN_TYPES = [
        ('positive', 'Positive'),
        ('warning', 'Warning'),
        ('neutral', 'Neutral'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='detected_patterns')
    title = models.CharField(max_length=100)
    description = models.TextField()
    confidence = models.CharField(max_length=10) # e.g., '85%'
    pattern_type = models.CharField(max_length=20, choices=PATTERN_TYPES, default='neutral')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for {self.user.username}"

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['order']
        verbose_name_plural = "FAQs"

class HowItWorksStep(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']

class AppConfig(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.TextField()
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.key

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=20) # e.g. "5 min"
    difficulty = models.CharField(max_length=20) # e.g. "Easy", "Medium"
    type = models.CharField(max_length=50) # e.g. "Breathing", "Journaling", "Meditation"
    image_tag = models.CharField(max_length=20) # e.g. "img_54"
    action_text = models.CharField(max_length=50, default="Start Now →")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for {self.user.username}"

class PasswordResetOTP(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_otps', null=True, blank=True)
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    expiry_time = models.DateTimeField()
    attempts = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.email} - {self.otp}"

class PasswordResetLog(models.Model):
    email = models.EmailField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50) # 'REQUEST', 'VERIFY_FAIL', 'RESET_SUCCESS'
    
    class Meta:
        ordering = ['-timestamp']
