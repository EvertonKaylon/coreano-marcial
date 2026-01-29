"""
Admin configuration for progress models.
"""
from django.contrib import admin
from .models import UserProgress, LessonProgress, VocabularyMastery


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    """
    Admin for UserProgress model.
    """
    list_display = ['user', 'current_belt', 'total_lessons_completed', 'total_vocabulary_mastered', 'overall_accuracy']
    list_filter = ['current_belt', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    """
    Admin for LessonProgress model.
    """
    list_display = ['user', 'lesson', 'completed', 'times_practiced', 'last_practiced_at']
    list_filter = ['completed', 'lesson__belt_level', 'created_at']
    search_fields = ['user__username', 'lesson__title_portuguese']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(VocabularyMastery)
class VocabularyMasteryAdmin(admin.ModelAdmin):
    """
    Admin for VocabularyMastery model.
    """
    list_display = ['user', 'vocabulary', 'mastery_level', 'times_reviewed', 'last_reviewed_at']
    list_filter = ['mastery_level', 'created_at']
    search_fields = ['user__username', 'vocabulary__korean_text', 'vocabulary__portuguese_translation']
    readonly_fields = ['created_at', 'updated_at']
