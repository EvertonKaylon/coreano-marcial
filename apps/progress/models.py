"""
Models for user progress tracking.
"""
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.lessons.models import BeltLevel, Lesson, VocabularyItem


class UserProgress(models.Model):
    """
    Tracks overall user progress.
    One-to-one relationship with User.
    """
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progress',
        verbose_name='Usuário'
    )
    current_belt = models.ForeignKey(
        BeltLevel,
        on_delete=models.PROTECT,
        related_name='current_users',
        verbose_name='Faixa Atual'
    )
    total_lessons_completed = models.PositiveIntegerField(
        default=0,
        verbose_name='Total de Lições Completadas'
    )
    total_vocabulary_mastered = models.PositiveIntegerField(
        default=0,
        verbose_name='Total de Vocabulário Dominado'
    )
    overall_accuracy = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        verbose_name='Acurácia Geral',
        help_text='Será calculado na Fase 3 com pronunciation assessment'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Progresso do Usuário'
        verbose_name_plural = 'Progressos dos Usuários'
    
    def __str__(self):
        return f"{self.user.username} - {self.current_belt.name_portuguese}"
    
    def can_advance_to_next_belt(self):
        """
        Check if user meets criteria to advance to the next belt level.
        Returns tuple: (can_advance: bool, next_belt: BeltLevel or None)
        """
        next_belt = BeltLevel.objects.filter(order=self.current_belt.order + 1).first()
        
        if not next_belt:
            return False, None
        
        completed_lessons_count = LessonProgress.objects.filter(
            user=self.user,
            completed=True,
            lesson__belt_level=self.current_belt
        ).count()
        
        mastered_vocab_count = VocabularyMastery.objects.filter(
            user=self.user,
            mastery_level__gte=4
        ).count()
        
        meets_lessons = completed_lessons_count >= self.current_belt.min_lessons_completed
        meets_vocab = mastered_vocab_count >= self.current_belt.min_vocabulary_mastered
        meets_accuracy = self.overall_accuracy >= self.current_belt.min_accuracy_percentage
        
        can_advance = meets_lessons and meets_vocab and meets_accuracy
        
        return can_advance, next_belt


class LessonProgress(models.Model):
    """
    Tracks progress on individual lessons.
    """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lesson_progress',
        verbose_name='Usuário'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='user_progress',
        verbose_name='Lição'
    )
    completed = models.BooleanField(
        default=False,
        verbose_name='Completada'
    )
    times_practiced = models.PositiveIntegerField(
        default=0,
        verbose_name='Vezes Praticadas'
    )
    last_practiced_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Última Prática'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Progresso de Lição'
        verbose_name_plural = 'Progressos de Lições'
        unique_together = [['user', 'lesson']]
    
    def __str__(self):
        status = 'Completada' if self.completed else 'Em Progresso'
        return f"{self.user.username} - {self.lesson.title_portuguese} ({status})"


class VocabularyMastery(models.Model):
    """
    Tracks mastery level of vocabulary items per user.
    """
    
    MASTERY_LEVELS = [
        (1, 'Iniciante'),
        (2, 'Básico'),
        (3, 'Intermediário'),
        (4, 'Proficiente'),
        (5, 'Mestre'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vocabulary_mastery',
        verbose_name='Usuário'
    )
    vocabulary = models.ForeignKey(
        VocabularyItem,
        on_delete=models.CASCADE,
        related_name='user_mastery',
        verbose_name='Vocabulário'
    )
    mastery_level = models.IntegerField(
        choices=MASTERY_LEVELS,
        default=1,
        verbose_name='Nível de Domínio'
    )
    times_reviewed = models.PositiveIntegerField(
        default=0,
        verbose_name='Vezes Revisadas'
    )
    last_reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Última Revisão'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Domínio de Vocabulário'
        verbose_name_plural = 'Domínios de Vocabulário'
        unique_together = [['user', 'vocabulary']]
    
    def __str__(self):
        return f"{self.user.username} - {self.vocabulary.korean_text} (Nível {self.mastery_level})"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_progress(sender, instance, created, **kwargs):
    """
    Automatically create UserProgress when a User is created.
    Assigns first belt level (order=1).
    """
    if created:
        first_belt = BeltLevel.objects.filter(order=1).first()
        if not first_belt:
            import logging
            logger = logging.getLogger('django')
            logger.critical("No first belt found during user creation.")
            return
        UserProgress.objects.create(user=instance, current_belt=first_belt)
