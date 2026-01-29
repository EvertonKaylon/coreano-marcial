"""
Admin configuration for lessons and vocabulary.
"""
from django.contrib import admin
from .models import BeltLevel, Lesson, VocabularyItem


@admin.register(BeltLevel)
class BeltLevelAdmin(admin.ModelAdmin):
    """
    Admin for BeltLevel model.
    """
    list_display = ['order', 'name_portuguese', 'name_korean', 'min_lessons_completed', 'min_vocabulary_mastered']
    list_editable = ['min_lessons_completed', 'min_vocabulary_mastered']
    ordering = ['order']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Admin for Lesson model.
    """
    list_display = ['belt_level', 'order_in_belt', 'title_portuguese', 'title_korean', 'created_at']
    list_filter = ['belt_level', 'created_at']
    search_fields = ['title_korean', 'title_portuguese', 'description']
    ordering = ['belt_level__order', 'order_in_belt']


@admin.register(VocabularyItem)
class VocabularyItemAdmin(admin.ModelAdmin):
    """
    Admin for VocabularyItem model.
    """
    list_display = ['korean_text', 'portuguese_translation', 'difficulty', 'created_at']
    list_filter = ['difficulty', 'created_at']
    search_fields = ['korean_text', 'portuguese_translation', 'context']
    filter_horizontal = ['lessons']
