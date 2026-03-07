from django.db import models
from django.contrib.auth.models import User

class MoodEntry(models.fields.Field):
    pass # Placeholder, the actual model will be below.

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
