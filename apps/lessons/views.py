"""
Views for lessons and belt levels.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import BeltLevel, Lesson


class HomeView(LoginRequiredMixin, ListView):
    """
    Home page showing all belt levels.
    """
    model = BeltLevel
    template_name = 'lessons/home.html'
    context_object_name = 'belt_levels'


class BeltDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for a specific belt level, showing all lessons.
    """
    model = BeltLevel
    template_name = 'lessons/belt_detail.html'
    context_object_name = 'belt_level'
    pk_url_kwarg = 'belt_id'


class LessonDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for a specific lesson, showing vocabulary and audio.
    """
    model = Lesson
    template_name = 'lessons/lesson_detail.html'
    context_object_name = 'lesson'
    pk_url_kwarg = 'lesson_id'
