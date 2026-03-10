from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar_name = models.CharField(max_length=100, default='default_avatar')
    language = models.CharField(max_length=20, default='English')
    text_size = models.CharField(max_length=20, default='Medium')
    notifications_enabled = models.BooleanField(default=True)
    notification_time = models.TimeField(null=True, blank=True)
    mental_health_score = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    goals = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

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

    class Meta:
        ordering = ['-timestampMillis']

class ChatMessage(models.Model):
    MODE_CHOICES = [
        ('Calm', 'Calm'),
        ('CBT', 'CBT Coach'),
        ('Listener', 'Listener'),
        ('General', 'General'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    text = models.TextField()
    is_user = models.BooleanField(default=True)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='General')
    language = models.CharField(max_length=20, default='English')
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

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.timestamp}"
