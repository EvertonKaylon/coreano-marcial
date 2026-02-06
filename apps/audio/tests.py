from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.audio.models import AudioFile
from apps.lessons.models import BeltLevel, Lesson, VocabularyItem


class AudioFileValidationTests(TestCase):
    def setUp(self):
        self.belt = BeltLevel.objects.create(
            name_korean='흰띠',
            name_portuguese='Branca',
            order=1,
        )
        self.lesson = Lesson.objects.create(
            belt_level=self.belt,
            title_korean='기본 인사',
            title_portuguese='Saudação Básica',
            order_in_belt=1,
        )
        self.vocabulary = VocabularyItem.objects.create(
            korean_text='차렷',
            portuguese_translation='Atenção',
        )

    def _audio_file(self, name='audio.mp3'):
        return SimpleUploadedFile(name, b'fake-audio-content', content_type='audio/mpeg')

    def test_lesson_audio_valid(self):
        audio = AudioFile(
            audio_type='lesson',
            lesson=self.lesson,
            audio_file=self._audio_file(),
        )
        audio.full_clean()  # must not raise

    def test_vocabulary_audio_valid(self):
        audio = AudioFile(
            audio_type='vocabulary',
            vocabulary=self.vocabulary,
            audio_file=self._audio_file(),
        )
        audio.full_clean()  # must not raise

    def test_both_relationships_invalid(self):
        audio = AudioFile(
            audio_type='lesson',
            lesson=self.lesson,
            vocabulary=self.vocabulary,
            audio_file=self._audio_file(),
        )
        with self.assertRaises(ValidationError):
            audio.full_clean()

    def test_no_relationship_invalid(self):
        audio = AudioFile(
            audio_type='lesson',
            audio_file=self._audio_file(),
        )
        with self.assertRaises(ValidationError):
            audio.full_clean()

    def test_lesson_type_with_vocabulary_only_invalid(self):
        audio = AudioFile(
            audio_type='lesson',
            vocabulary=self.vocabulary,
            audio_file=self._audio_file(),
        )
        with self.assertRaises(ValidationError):
            audio.full_clean()

    def test_vocabulary_type_with_lesson_only_invalid(self):
        audio = AudioFile(
            audio_type='vocabulary',
            lesson=self.lesson,
            audio_file=self._audio_file(),
        )
        with self.assertRaises(ValidationError):
            audio.full_clean()
