"""
Models for audio file storage and serving.
"""
from django.core.exceptions import ValidationError
from django.db import models
from apps.lessons.models import Lesson, VocabularyItem


def validate_audio_extension(value):
    """
    Validate that uploaded file is an audio file (.mp3, .ogg, .opus).
    """
    import os
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.mp3', '.ogg', '.opus']
    if ext not in valid_extensions:
        raise ValidationError(f'Tipo de arquivo não suportado. Use: {", ".join(valid_extensions)}')


class AudioFile(models.Model):
    """
    Audio file for pronunciation examples.
    Can be associated with lessons or vocabulary items.
    """
    
    AUDIO_TYPE_CHOICES = [
        ('lesson', 'Lição'),
        ('vocabulary', 'Vocabulário'),
    ]
    
    audio_type = models.CharField(
        max_length=20,
        choices=AUDIO_TYPE_CHOICES,
        verbose_name='Tipo de Áudio'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='audio_files',
        null=True,
        blank=True,
        verbose_name='Lição'
    )
    vocabulary = models.ForeignKey(
        VocabularyItem,
        on_delete=models.CASCADE,
        related_name='audio_files',
        null=True,
        blank=True,
        verbose_name='Vocabulário'
    )
    audio_file = models.FileField(
        upload_to='audio/%Y/%m/',
        validators=[validate_audio_extension],
        verbose_name='Arquivo de Áudio'
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Descrição',
        help_text='Descrição opcional do áudio'
    )
    duration_seconds = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Duração (segundos)',
        help_text='Duração do áudio em segundos (opcional)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Arquivo de Áudio'
        verbose_name_plural = 'Arquivos de Áudio'
        ordering = ['-created_at']
    
    def __str__(self):
        if self.lesson:
            return f"Áudio: {self.lesson.title_portuguese}"
        elif self.vocabulary:
            return f"Áudio: {self.vocabulary.korean_text}"
        return f"Áudio #{self.id}"
    
    def clean(self):
        """
        Validate relationship consistency with audio_type.
        """
        if self.lesson and self.vocabulary:
            raise ValidationError('Áudio não pode estar associado a lição E vocabulário ao mesmo tempo.')

        if not self.lesson and not self.vocabulary:
            raise ValidationError('Áudio deve estar associado a uma lição OU a um vocabulário.')

        if self.audio_type == 'lesson' and not self.lesson:
            raise ValidationError('Lição deve ser especificada para áudio do tipo "Lição".')

        if self.audio_type == 'lesson' and self.vocabulary:
            raise ValidationError('Áudio do tipo "Lição" não pode estar associado a vocabulário.')

        if self.audio_type == 'vocabulary' and not self.vocabulary:
            raise ValidationError('Vocabulário deve ser especificado para áudio do tipo "Vocabulário".')

        if self.audio_type == 'vocabulary' and self.lesson:
            raise ValidationError('Áudio do tipo "Vocabulário" não pode estar associado a lição.')
