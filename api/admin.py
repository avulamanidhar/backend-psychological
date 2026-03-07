from django.contrib import admin
from .models import MoodEntry

@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ('moodName', 'intensity', 'timestampMillis', 'user')
    search_fields = ('moodName', 'journal')
    list_filter = ('moodName', 'intensity')
