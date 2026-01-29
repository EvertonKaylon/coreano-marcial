"""
Models for lessons, vocabulary, and belt levels.
"""
from django.db import models


class BeltLevel(models.Model):
    """
    Belt levels (faixas) for martial arts progression.
    Examples: Branca, Amarela, Laranja, Verde, Azul, Roxa, Marrom, Preta.
    """
    
    name_korean = models.CharField(
        max_length=50,
        verbose_name='Nome em Coreano',
        help_text='Nome da faixa em Hangul (ex: 흰띠)'
    )
    name_portuguese = models.CharField(
        max_length=50,
        verbose_name='Nome em Português',
        help_text='Nome da faixa em português (ex: Branca)'
    )
    order = models.PositiveIntegerField(
        unique=True,
        verbose_name='Ordem',
        help_text='Ordem de progressão (1=primeira faixa, 8=última)'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descrição',
        help_text='Descrição opcional da faixa'
    )
    min_lessons_completed = models.PositiveIntegerField(
        default=0,
        verbose_name='Mínimo de Lições Completadas',
        help_text='Número mínimo de lições que devem ser completadas para avançar desta faixa'
    )
    min_vocabulary_mastered = models.PositiveIntegerField(
        default=0,
        verbose_name='Mínimo de Vocabulário Dominado',
        help_text='Número mínimo de vocabulário dominado para avançar desta faixa'
    )
    min_accuracy_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        verbose_name='Porcentagem Mínima de Acurácia',
        help_text='Acurácia mínima (0-100) para avançar desta faixa. Usado na Fase 3.'
    )
    
    class Meta:
        verbose_name = 'Nível de Faixa'
        verbose_name_plural = 'Níveis de Faixa'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.name_portuguese} ({self.name_korean})"


class Lesson(models.Model):
    """
    A lesson belonging to a specific belt level.
    Contains vocabulary items and audio.
    """
    
    belt_level = models.ForeignKey(
        BeltLevel,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Nível de Faixa'
    )
    title_korean = models.CharField(
        max_length=200,
        verbose_name='Título em Coreano',
        help_text='Título da lição em Hangul'
    )
    title_portuguese = models.CharField(
        max_length=200,
        verbose_name='Título em Português',
        help_text='Título da lição em português'
    )
    order_in_belt = models.PositiveIntegerField(
        verbose_name='Ordem na Faixa',
        help_text='Ordem da lição dentro da faixa'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descrição',
        help_text='Descrição opcional da lição'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lição'
        verbose_name_plural = 'Lições'
        ordering = ['belt_level__order', 'order_in_belt']
        unique_together = [['belt_level', 'order_in_belt']]
    
    def __str__(self):
        return f"{self.belt_level.name_portuguese} - {self.title_portuguese}"


class VocabularyItem(models.Model):
    """
    A vocabulary item (word or phrase) in Korean.
    Can belong to one or more lessons.
    """
    
    DIFFICULTY_CHOICES = [
        (1, 'Básico'),
        (2, 'Intermediário'),
        (3, 'Avançado'),
    ]
    
    korean_text = models.CharField(
        max_length=100,
        verbose_name='Texto em Coreano',
        help_text='Palavra ou frase em Hangul (SEM romanização)'
    )
    portuguese_translation = models.CharField(
        max_length=200,
        verbose_name='Tradução em Português',
        help_text='Tradução para português'
    )
    context = models.TextField(
        blank=True,
        verbose_name='Contexto',
        help_text='Contexto de uso (opcional)'
    )
    example_sentence_korean = models.TextField(
        blank=True,
        verbose_name='Exemplo em Coreano',
        help_text='Frase de exemplo em Hangul (opcional)'
    )
    example_sentence_portuguese = models.TextField(
        blank=True,
        verbose_name='Exemplo em Português',
        help_text='Tradução do exemplo (opcional)'
    )
    difficulty = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        default=1,
        verbose_name='Dificuldade'
    )
    lessons = models.ManyToManyField(
        Lesson,
        related_name='vocabulary_items',
        verbose_name='Lições'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Item de Vocabulário'
        verbose_name_plural = 'Itens de Vocabulário'
        ordering = ['korean_text']
    
    def __str__(self):
        return f"{self.korean_text} ({self.portuguese_translation})"
