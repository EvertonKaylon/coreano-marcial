"""
Admin configuration for audio files.
"""
from django.contrib import admin
from .models import AudioFile


@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    """
    Admin for AudioFile model.
    """
    list_display = ['id', 'audio_type', 'lesson', 'vocabulary', 'duration_seconds', 'created_at']
    list_filter = ['audio_type', 'created_at']
    search_fields = ['description', 'lesson__title_portuguese', 'vocabulary__korean_text']
    readonly_fields = ['created_at', 'updated_at']
