"""
Views for progress tracking and dashboard.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from .models import UserProgress, LessonProgress, VocabularyMastery


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    User progress dashboard showing current belt, stats, and advancement criteria.
    """
    template_name = 'progress/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_progress = get_object_or_404(UserProgress, user=self.request.user)
        
        can_advance, next_belt = user_progress.can_advance_to_next_belt()
        
        completed_lessons = LessonProgress.objects.filter(
            user=self.request.user,
            completed=True,
            lesson__belt_level=user_progress.current_belt
        ).count()
        
        mastered_vocab = VocabularyMastery.objects.filter(
            user=self.request.user,
            mastery_level__gte=4
        ).count()
        
        context['user_progress'] = user_progress
        context['can_advance'] = can_advance
        context['next_belt'] = next_belt
        context['completed_lessons'] = completed_lessons
        context['mastered_vocab'] = mastered_vocab
        
        return context


@login_required
def advance_belt(request):
    """
    Advance user to next belt if criteria are met.
    """
    if request.method == 'POST':
        user_progress = get_object_or_404(UserProgress, user=request.user)
        can_advance, next_belt = user_progress.can_advance_to_next_belt()
        
        if can_advance and next_belt:
            user_progress.current_belt = next_belt
            user_progress.save()
            messages.success(request, f'Parabéns! Você avançou para a faixa {next_belt.name_portuguese}!')
        else:
            messages.error(request, 'Você ainda não atende aos critérios para avançar de faixa.')
        
        return redirect('progress:dashboard')
    
    return redirect('progress:dashboard')
