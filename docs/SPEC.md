# SPEC v0.1 — Coreano Marcial: Korean Language Learning for Martial Arts

**Version:** 1.0  
**Date:** January 27, 2026  
**Source Document:** PRD.md v1.0  
**Status:** Planning Phase - Implementation Not Started

---

## Visão Geral

Sistema de ensino de idioma coreano contextualizado para artes marciais, implementado como Progressive Web Application (PWA) server-driven usando Django + HTMX. O sistema prioriza:

- **Audio-first methodology**: Pronúncia autêntica sem dependência de romanização
- **Offline capability**: PWA com Service Worker para uso sem conexão
- **Hierarchical progression**: Sistema de progressão baseado em faixas de artes marciais
- **Mobile-first**: Interface otimizada para dispositivos móveis
- **Security-first**: AppSec e DevSecOps desde o início

**Stack Técnico:**
- Backend: Django (Python)
- Frontend: HTMX (14KB) para atualizações parciais de DOM
- PWA: Service Worker + Manifest
- Storage: PostgreSQL (banco de dados), File storage para áudio
- Optional: Alpine.js (15KB) para interatividade client-side mínima

**Abordagem de Desenvolvimento:**
Implementação faseada conforme definido no PRD (Seção 6):
- **Fase 0**: Django app básico sem PWA
- **Fase 1**: HTMX + Partial rendering
- **Fase 2**: Service Worker + Offline mode
- **Fase 3**: Pronunciation API integration (opcional, dependendo de validação)

---

## Escopo

### O que será implementado:

**Fase 0 (Esta SPEC):**
1. Estrutura Django base com apps modularizados
2. Sistema de autenticação de usuários
3. Modelo de dados para lições, vocabulário e progressão
4. Views Django básicas (full-page rendering, sem HTMX ainda)
5. Templates HTML base
6. Sistema de armazenamento e serving de arquivos de áudio
7. Sistema de progressão baseado em faixas (belt levels)
8. Configurações de segurança básicas (HTTPS, CSRF, SECRET_KEY em variável de ambiente)

**Fase 1 (Fora desta SPEC, mas planejada):**
- Integração HTMX para partial rendering
- Fragmentos de templates (_partials)
- Views duplicadas (full page + HTMX fragments)

**Fase 2 (Fora desta SPEC, mas planejada):**
- Service Worker para offline capability
- PWA Manifest
- Cache management

**Fase 3 (Fora desta SPEC, mas planejada):**
- Integração com Pronunciation Assessment API (Azure/Speechace/SpeechSuper)

### O que explicitamente não será implementado nesta SPEC:

- ❌ HTMX integration (Fase 1)
- ❌ Service Worker / PWA offline mode (Fase 2)
- ❌ Pronunciation assessment API (Fase 3)
- ❌ Gamification features (pontos, streaks)
- ❌ Social/community features
- ❌ Analytics tracking
- ❌ Content Management System (CMS) - conteúdo será gerenciado via Django Admin
- ❌ Mobile native apps
- ❌ Romanização de qualquer tipo (decisão pedagógica do PRD)
- ❌ Multi-idioma (apenas coreano-português inicialmente)

---

## Arquivos Afetados

### 1. `config/settings.py`

**Tipo:** ( ) Criar (X) Modificar

**Responsabilidade do arquivo:**  
Configurações centrais do projeto Django. Controla segurança, middleware, apps instalados, banco de dados, arquivos estáticos, internacionalização.

**O que fazer neste arquivo:**

1. **Configurações de Segurança (PRD Seção 9):**
   ```python
   # SECRET_KEY deve vir de variável de ambiente
   SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
   if not SECRET_KEY:
       raise ValueError("DJANGO_SECRET_KEY environment variable not set")
   
   # DEBUG = False em produção (checklist PRD linha 851)
   DEBUG = os.environ.get('DEBUG', 'False') == 'True'
   
   # ALLOWED_HOSTS restrito (checklist PRD linha 853)
   ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
   ```

2. **Apps Instalados:**
   ```python
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       # Project apps (PRD Seção 2.1, linhas 156-188)
       'apps.lessons',
       'apps.progress',
       'apps.audio',
       'apps.users',  # Custom user app
   ]
   ```

3. **Middleware de Segurança (PRD Seção 4.1):**
   ```python
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.middleware.common.CommonMiddleware',
       'django.middleware.csrf.CsrfViewMiddleware',  # CSRF ativo (linha 854)
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'django.contrib.messages.middleware.MessageMiddleware',
       'django.middleware.clickjacking.XFrameOptionsMiddleware',
   ]
   ```

4. **Content Security Policy Headers (PRD linhas 211-226):**
   ```python
   # Instalar django-csp
   MIDDLEWARE += ['csp.middleware.CSPMiddleware']
   
   CSP_DEFAULT_SRC = ("'self'",)
   CSP_SCRIPT_SRC = ("'self'",)
   CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")  # Permitir estilos inline
   CSP_IMG_SRC = ("'self'", "data:")
   CSP_FONT_SRC = ("'self'",)
   CSP_CONNECT_SRC = ("'self'",)
   CSP_MEDIA_SRC = ("'self'",)  # Para arquivos de áudio
   ```

5. **Configuração de Sessão Segura (PRD linha 856):**
   ```python
   SESSION_COOKIE_SECURE = True  # Apenas HTTPS
   SESSION_COOKIE_HTTPONLY = True  # Não acessível via JavaScript
   SESSION_COOKIE_SAMESITE = 'Strict'  # Proteção CSRF adicional
   CSRF_COOKIE_SECURE = True
   CSRF_COOKIE_HTTPONLY = True
   CSRF_COOKIE_SAMESITE = 'Strict'
   ```

6. **Banco de Dados (PostgreSQL):**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': os.environ.get('DB_NAME'),
           'USER': os.environ.get('DB_USER'),
           'PASSWORD': os.environ.get('DB_PASSWORD'),
           'HOST': os.environ.get('DB_HOST', 'localhost'),
           'PORT': os.environ.get('DB_PORT', '5432'),
       }
   }
   ```

7. **Arquivos Estáticos e Media (PRD linhas 182-188):**
   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   STATICFILES_DIRS = [
       os.path.join(BASE_DIR, 'static'),
   ]
   
   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
   ```

8. **Internacionalização:**
   ```python
   LANGUAGE_CODE = 'pt-br'  # Interface em português
   TIME_ZONE = 'America/Sao_Paulo'
   USE_I18N = True
   USE_TZ = True
   ```

9. **Logging (PRD linha 864):**
   ```python
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'formatters': {
           'verbose': {
               'format': '{levelname} {asctime} {module} {message}',
               'style': '{',
           },
       },
       'handlers': {
           'file': {
               'level': 'INFO',
               'class': 'logging.FileHandler',
               'filename': os.path.join(BASE_DIR, 'logs/django.log'),
               'formatter': 'verbose',
           },
           'security_file': {
               'level': 'WARNING',
               'class': 'logging.FileHandler',
               'filename': os.path.join(BASE_DIR, 'logs/security.log'),
               'formatter': 'verbose',
           },
       },
       'loggers': {
           'django': {
               'handlers': ['file'],
               'level': 'INFO',
               'propagate': True,
           },
           'django.security': {
               'handlers': ['security_file'],
               'level': 'WARNING',
               'propagate': False,
           },
       },
   }
   ```

**Referências do PRD:**
- Seção 2.1 (linhas 156-188): Estrutura de arquivos Django
- Seção 4.1 (linhas 211-226): CSP Headers
- Seção 9 (linhas 846-868): Security Checklist

---

### 2. `config/urls.py`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
URL routing principal do projeto Django. Direciona requisições HTTP para os apps apropriados.

**O que fazer neste arquivo:**

1. **Importações necessárias:**
   ```python
   from django.contrib import admin
   from django.urls import path, include
   from django.conf import settings
   from django.conf.urls.static import static
   ```

2. **URL Patterns:**
   ```python
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('accounts/', include('django.contrib.auth.urls')),  # Login/logout
       path('', include('apps.lessons.urls')),  # Homepage e lições
       path('progress/', include('apps.progress.urls')),
       path('audio/', include('apps.audio.urls')),
   ]
   ```

3. **Serving de Media Files em desenvolvimento:**
   ```python
   if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

**Referências do PRD:**
- Seção 2.1 (linha 159): URL routing structure
- Seção 2.1 (linhas 111-123): "HTMX requires a lot more URLs" - preparar estrutura modular desde o início

---

### 3. `apps/lessons/models.py`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
Define os modelos de dados para lições, vocabulário, frases e conteúdo educacional.

**O que fazer neste arquivo:**

1. **Modelo BeltLevel (PRD linhas 362-388):**
   ```python
   from django.db import models
   from django.core.validators import MinValueValidator, MaxValueValidator
   
   class BeltLevel(models.Model):
       """
       Representa níveis de progressão baseados em faixas de artes marciais.
       PRD: "Hierarchical progression modeling traditional martial arts belt systems"
       """
       BELT_COLORS = [
           ('white', 'Branca'),
           ('yellow', 'Amarela'),
           ('green', 'Verde'),
           ('blue', 'Azul'),
           ('red', 'Vermelha'),
           ('black', 'Preta'),
       ]
       
       name = models.CharField(max_length=50)
       color = models.CharField(max_length=20, choices=BELT_COLORS)
       order = models.IntegerField(unique=True)  # 1 = White, 6 = Black
       korean_name = models.CharField(max_length=100)  # Ex: "하얀띠" (Hayan-tti)
       description = models.TextField()
       
       # Critérios de avanço (PRD linha 369)
       min_lessons_completed = models.IntegerField(default=0)
       min_vocabulary_mastered = models.IntegerField(default=0)
       min_accuracy_percentage = models.DecimalField(
           max_digits=5, 
           decimal_places=2,
           validators=[MinValueValidator(0), MaxValueValidator(100)],
           default=70.0
       )
       
       class Meta:
           ordering = ['order']
       
       def __str__(self):
           return f"{self.get_color_display()} ({self.korean_name})"
   ```

2. **Modelo Lesson:**
   ```python
   class Lesson(models.Model):
       """
       Uma lição individual focada em um tópico específico.
       PRD: "20 lessons, simple progression" (linha 914)
       """
       title = models.CharField(max_length=200)
       title_korean = models.CharField(max_length=200)  # Sem romanização
       belt_level = models.ForeignKey(BeltLevel, on_delete=models.CASCADE, related_name='lessons')
       order = models.IntegerField()  # Ordem dentro da faixa
       description = models.TextField()
       
       # Tema da lição (ex: "Cumprimentos", "Comandos básicos", "Contagem")
       theme = models.CharField(max_length=100)
       
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
       
       class Meta:
           ordering = ['belt_level__order', 'order']
           unique_together = ['belt_level', 'order']
       
       def __str__(self):
           return f"{self.title} ({self.belt_level.get_color_display()})"
   ```

3. **Modelo Vocabulary:**
   ```python
   class Vocabulary(models.Model):
       """
       Termo individual de vocabulário (palavra ou frase).
       PRD: "Zero romanization dependence" (linha 12)
       """
       lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='vocabulary')
       
       # Apenas Hangul, sem romanização
       korean_text = models.CharField(max_length=200)  # Ex: "안녕하세요"
       
       # Tradução em português
       portuguese_translation = models.CharField(max_length=200)  # Ex: "Olá"
       
       # Contexto de uso em artes marciais
       martial_arts_context = models.TextField(blank=True)  # Ex: "Cumprimento ao mestre"
       
       # Notas adicionais
       usage_notes = models.TextField(blank=True)
       
       # Arquivo de áudio será gerenciado por AudioFile model (relação será criada)
       
       order = models.IntegerField()  # Ordem dentro da lição
       
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
       
       class Meta:
           ordering = ['lesson', 'order']
           unique_together = ['lesson', 'order']
           verbose_name_plural = 'Vocabulary'
       
       def __str__(self):
           return f"{self.korean_text} ({self.portuguese_translation})"
   ```

**Referências do PRD:**
- Seção 3.1 (linhas 362-388): Belt-based progression model
- Linha 12: "zero romanization dependence"
- Linha 914: "20 lessons, simple progression"
- Seção 5.2 (linhas 454-491): Content structure

---

### 4. `apps/progress/models.py`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
Modelos para rastreamento de progresso do usuário, completude de lições e avanço de faixas.

**O que fazer neste arquivo:**

1. **Modelo UserProgress:**
   ```python
   from django.db import models
   from django.contrib.auth import get_user_model
   from apps.lessons.models import BeltLevel, Lesson, Vocabulary
   
   User = get_user_model()
   
   class UserProgress(models.Model):
       """
       Progresso geral do usuário no sistema.
       """
       user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='progress')
       current_belt = models.ForeignKey(BeltLevel, on_delete=models.PROTECT, related_name='users_at_this_level')
       
       # Estatísticas gerais
       total_lessons_completed = models.IntegerField(default=0)
       total_vocabulary_mastered = models.IntegerField(default=0)
       overall_accuracy = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
       
       # Timestamps
       started_at = models.DateTimeField(auto_now_add=True)
       last_activity = models.DateTimeField(auto_now=True)
       
       def __str__(self):
           return f"{self.user.username} - {self.current_belt}"
       
       def can_advance_to_next_belt(self):
           """
           Verifica se usuário atende critérios para próxima faixa.
           PRD linha 369: critérios de avanço baseados em lições, vocabulário e acurácia
           """
           next_belt = BeltLevel.objects.filter(order=self.current_belt.order + 1).first()
           if not next_belt:
               return False
           
           return (
               self.total_lessons_completed >= next_belt.min_lessons_completed and
               self.total_vocabulary_mastered >= next_belt.min_vocabulary_mastered and
               self.overall_accuracy >= next_belt.min_accuracy_percentage
           )
   ```

2. **Modelo LessonProgress:**
   ```python
   class LessonProgress(models.Model):
       """
       Progresso do usuário em uma lição específica.
       """
       STATUS_CHOICES = [
           ('not_started', 'Não Iniciada'),
           ('in_progress', 'Em Progresso'),
           ('completed', 'Completada'),
       ]
       
       user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
       lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')
       
       status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
       
       # Timestamps
       started_at = models.DateTimeField(null=True, blank=True)
       completed_at = models.DateTimeField(null=True, blank=True)
       last_accessed = models.DateTimeField(auto_now=True)
       
       class Meta:
           unique_together = ['user', 'lesson']
       
       def __str__(self):
           return f"{self.user.username} - {self.lesson.title} ({self.get_status_display()})"
   ```

3. **Modelo VocabularyMastery:**
   ```python
   class VocabularyMastery(models.Model):
       """
       Rastreamento de domínio de vocabulário individual.
       """
       MASTERY_LEVELS = [
           (1, 'Iniciante'),
           (2, 'Familiarizado'),
           (3, 'Competente'),
           (4, 'Proficiente'),
           (5, 'Mestre'),
       ]
       
       user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vocabulary_mastery')
       vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='user_mastery')
       
       mastery_level = models.IntegerField(choices=MASTERY_LEVELS, default=1)
       
       # Estatísticas de prática
       times_practiced = models.IntegerField(default=0)
       times_correct = models.IntegerField(default=0)
       last_practiced = models.DateTimeField(auto_now=True)
       
       class Meta:
           unique_together = ['user', 'vocabulary']
           verbose_name_plural = 'Vocabulary Mastery'
       
       def __str__(self):
           return f"{self.user.username} - {self.vocabulary.korean_text} (Nível {self.mastery_level})"
       
       @property
       def accuracy(self):
           """Calcula porcentagem de acerto."""
           if self.times_practiced == 0:
               return 0.0
           return (self.times_correct / self.times_practiced) * 100
   ```

**Referências do PRD:**
- Seção 3.1 (linhas 362-388): Belt progression system
- Linha 176: Progress models structure
- Seção 5.3 (linhas 492-522): Progress tracking requirements

---

### 5. `apps/audio/models.py`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
Gerenciamento de arquivos de áudio, metadados e relacionamento com vocabulário.

**O que fazer neste arquivo:**

1. **Modelo AudioFile:**
   ```python
   import os
   from django.db import models
   from django.core.validators import FileExtensionValidator
   from apps.lessons.models import Vocabulary
   
   def audio_upload_path(instance, filename):
       """
       Organiza arquivos de áudio por faixa e lição.
       Exemplo: audio/white_belt/lesson_1/greeting.mp3
       """
       belt_color = instance.vocabulary.lesson.belt_level.color
       lesson_id = instance.vocabulary.lesson.id
       return f'audio/{belt_color}_belt/lesson_{lesson_id}/{filename}'
   
   class AudioFile(models.Model):
       """
       Arquivo de áudio para pronúncia de vocabulário.
       PRD: "Audio-first methodology" (linha 12)
       PRD: "Audio files are large (1-5MB per high-quality pronunciation clip)" (linha 70)
       """
       vocabulary = models.OneToOneField(
           Vocabulary, 
           on_delete=models.CASCADE, 
           related_name='audio'
       )
       
       # Arquivo de áudio
       audio_file = models.FileField(
           upload_to=audio_upload_path,
           validators=[FileExtensionValidator(allowed_extensions=['mp3', 'ogg', 'opus'])],
           help_text='Formatos aceitos: MP3, OGG, Opus. Preferir Opus para melhor compressão.'
       )
       
       # Metadados
       duration_seconds = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
       file_size_bytes = models.BigIntegerField(null=True, blank=True)
       
       # Informações do speaker
       speaker_name = models.CharField(max_length=100, blank=True)
       speaker_gender = models.CharField(
           max_length=10, 
           choices=[('male', 'Masculino'), ('female', 'Feminino')],
           blank=True
       )
       recording_date = models.DateField(null=True, blank=True)
       
       # Qualidade
       sample_rate = models.IntegerField(null=True, blank=True, help_text='Hz (ex: 44100)')
       bitrate = models.IntegerField(null=True, blank=True, help_text='kbps (ex: 128)')
       
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
       
       def __str__(self):
           return f"Audio: {self.vocabulary.korean_text}"
       
       def save(self, *args, **kwargs):
           """
           Auto-populate file size on save.
           """
           if self.audio_file:
               self.file_size_bytes = self.audio_file.size
           super().save(*args, **kwargs)
   ```

2. **Signal para cleanup de arquivos órfãos:**
   ```python
   from django.db.models.signals import post_delete
   from django.dispatch import receiver
   
   @receiver(post_delete, sender=AudioFile)
   def delete_audio_file_on_delete(sender, instance, **kwargs):
       """
       Deleta arquivo físico quando AudioFile é deletado.
       PRD: Manutenção de arquivos de áudio (linha 840)
       """
       if instance.audio_file:
           if os.path.isfile(instance.audio_file.path):
               os.remove(instance.audio_file.path)
   ```

**Referências do PRD:**
- Linha 12: "audio-first methodology"
- Linha 70: "Audio files are large (1-5MB per high-quality pronunciation clip)"
- Linhas 179-181: Audio app structure
- Seção 2.3 (linhas 228-268): Audio handling best practices
- Linha 840: Audio content maintenance

---

### 6. `apps/users/models.py`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
Extensão do modelo de usuário padrão do Django para adicionar campos específicos do sistema.

**O que fazer neste arquivo:**

1. **Custom User Model (se necessário) ou Profile:**
   ```python
   from django.db import models
   from django.contrib.auth.models import User
   
   class UserProfile(models.Model):
       """
       Perfil estendido do usuário.
       Informações adicionais não cobertas pelo modelo User padrão.
       """
       user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
       
       # Preferências de aprendizado
       preferred_learning_pace = models.CharField(
           max_length=20,
           choices=[
               ('slow', 'Lento'),
               ('medium', 'Médio'),
               ('fast', 'Rápido'),
           ],
           default='medium'
       )
       
       # Contexto de artes marciais
       primary_martial_art = models.CharField(
           max_length=50,
           choices=[
               ('taekwondo', 'Taekwondo'),
               ('hapkido', 'Hapkido'),
               ('tang_soo_do', 'Tang Soo Do'),
               ('kuk_sool_won', 'Kuk Sool Won'),
               ('other', 'Outra'),
           ],
           blank=True
       )
       other_martial_art = models.CharField(max_length=100, blank=True)
       
       # Opções de interface
       show_audio_transcripts = models.BooleanField(
           default=False,
           help_text='Mostrar transcrição Hangul durante reprodução de áudio'
       )
       
       # Timezone para tracking correto
       timezone = models.CharField(max_length=50, default='America/Sao_Paulo')
       
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
       
       def __str__(self):
           return f"Profile: {self.user.username}"
   ```

2. **Signal para criar profile automaticamente:**
   ```python
   from django.db.models.signals import post_save
   from django.dispatch import receiver
   
   @receiver(post_save, sender=User)
   def create_user_profile(sender, instance, created, **kwargs):
       """Cria UserProfile automaticamente quando User é criado."""
       if created:
           UserProfile.objects.create(user=instance)
   
   @receiver(post_save, sender=User)
   def save_user_profile(sender, instance, **kwargs):
       """Salva UserProfile quando User é salvo."""
       instance.profile.save()
   ```

**Referências do PRD:**
- Linha 176: User models structure
- Seção 5.3 (linhas 492-522): User preferences and customization

---

### 7. `apps/lessons/views.py`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
Views Django para renderização de páginas de lições. FASE 0: apenas full-page rendering, sem HTMX.

**O que fazer neste arquivo:**

1. **Homepage View:**
   ```python
   from django.shortcuts import render, get_object_or_404
   from django.contrib.auth.decorators import login_required
   from .models import BeltLevel, Lesson
   from apps.progress.models import UserProgress, LessonProgress
   
   def home(request):
       """
       Homepage - mostra visão geral do sistema.
       Não requer autenticação.
       """
       belt_levels = BeltLevel.objects.all()[:3]  # Primeiras 3 faixas para preview
       
       context = {
           'belt_levels': belt_levels,
       }
       return render(request, 'lessons/home.html', context)
   ```

2. **Belt Level List View:**
   ```python
   @login_required
   def belt_level_list(request):
       """
       Lista todas as faixas disponíveis com progresso do usuário.
       """
       belt_levels = BeltLevel.objects.prefetch_related('lessons').all()
       user_progress = UserProgress.objects.get_or_create(user=request.user)[0]
       
       context = {
           'belt_levels': belt_levels,
           'user_progress': user_progress,
       }
       return render(request, 'lessons/belt_level_list.html', context)
   ```

3. **Lesson List View (para uma faixa):**
   ```python
   @login_required
   def lesson_list(request, belt_id):
       """
       Lista lições de uma faixa específica.
       PRD: "20 lessons, simple progression" (linha 914)
       """
       belt_level = get_object_or_404(BeltLevel, id=belt_id)
       lessons = belt_level.lessons.all()
       
       # Pegar progresso do usuário em cada lição
       user_progress_qs = LessonProgress.objects.filter(
           user=request.user,
           lesson__in=lessons
       ).select_related('lesson')
       
       # Criar dict de progresso por lesson_id
       progress_dict = {lp.lesson_id: lp for lp in user_progress_qs}
       
       # Adicionar progresso a cada lição
       for lesson in lessons:
           lesson.user_progress = progress_dict.get(lesson.id)
       
       context = {
           'belt_level': belt_level,
           'lessons': lessons,
       }
       return render(request, 'lessons/lesson_list.html', context)
   ```

4. **Lesson Detail View:**
   ```python
   @login_required
   def lesson_detail(request, lesson_id):
       """
       Detalhe de uma lição específica com vocabulário.
       Marca lição como "iniciada" se for primeiro acesso.
       """
       lesson = get_object_or_404(Lesson.objects.prefetch_related('vocabulary__audio'), id=lesson_id)
       
       # Criar ou atualizar progresso da lição
       lesson_progress, created = LessonProgress.objects.get_or_create(
           user=request.user,
           lesson=lesson
       )
       
       if created or lesson_progress.status == 'not_started':
           from django.utils import timezone
           lesson_progress.status = 'in_progress'
           lesson_progress.started_at = timezone.now()
           lesson_progress.save()
       
       # Pegar vocabulário da lição
       vocabulary_items = lesson.vocabulary.all()
       
       context = {
           'lesson': lesson,
           'lesson_progress': lesson_progress,
           'vocabulary_items': vocabulary_items,
       }
       return render(request, 'lessons/lesson_detail.html', context)
   ```

5. **Vocabulary Practice View:**
   ```python
   @login_required
   def vocabulary_practice(request, lesson_id):
       """
       Interface de prática de vocabulário (ouvir áudio e responder).
       FASE 0: apenas mostrar vocabulário com áudio.
       Pronunciation assessment será adicionado na Fase 3.
       """
       lesson = get_object_or_404(Lesson, id=lesson_id)
       vocabulary_items = lesson.vocabulary.select_related('audio').all()
       
       context = {
           'lesson': lesson,
           'vocabulary_items': vocabulary_items,
       }
       return render(request, 'lessons/vocabulary_practice.html', context)
   ```

**Referências do PRD:**
- Seção 2.1 (linhas 126-139): View pattern for Django
- Linha 914: "20 lessons, simple progression"
- Seção 5.1 (linhas 425-453): User flow through lessons

---

### 8. `apps/lessons/urls.py`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
URL patterns para o app de lições.

**O que fazer neste arquivo:**

```python
from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.home, name='home'),
    path('belts/', views.belt_level_list, name='belt_level_list'),
    path('belts/<int:belt_id>/lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/<int:lesson_id>/practice/', views.vocabulary_practice, name='vocabulary_practice'),
]
```

**Referências do PRD:**
- Seção 2.1 (linha 164): URL structure
- Seção 2.1 (linhas 111-123): URL organization warning

---

### 9. `apps/progress/views.py`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
Views para dashboard de progresso do usuário e avanço de faixas.

**O que fazer neste arquivo:**

1. **Dashboard View:**
   ```python
   from django.shortcuts import render, redirect
   from django.contrib.auth.decorators import login_required
   from django.contrib import messages
   from .models import UserProgress, LessonProgress, VocabularyMastery
   from apps.lessons.models import BeltLevel
   
   @login_required
   def progress_dashboard(request):
       """
       Dashboard geral de progresso do usuário.
       Mostra faixa atual, estatísticas, próxima faixa.
       """
       user_progress, created = UserProgress.objects.get_or_create(
           user=request.user,
           defaults={'current_belt': BeltLevel.objects.first()}
       )
       
       # Estatísticas de lições
       completed_lessons = LessonProgress.objects.filter(
           user=request.user,
           status='completed'
       ).count()
       
       in_progress_lessons = LessonProgress.objects.filter(
           user=request.user,
           status='in_progress'
       ).count()
       
       # Estatísticas de vocabulário
       mastered_vocab = VocabularyMastery.objects.filter(
           user=request.user,
           mastery_level__gte=4  # Proficiente ou Mestre
       ).count()
       
       # Próxima faixa
       next_belt = BeltLevel.objects.filter(
           order=user_progress.current_belt.order + 1
       ).first()
       
       # Verificar se pode avançar
       can_advance = user_progress.can_advance_to_next_belt() if next_belt else False
       
       context = {
           'user_progress': user_progress,
           'completed_lessons': completed_lessons,
           'in_progress_lessons': in_progress_lessons,
           'mastered_vocab': mastered_vocab,
           'next_belt': next_belt,
           'can_advance': can_advance,
       }
       return render(request, 'progress/dashboard.html', context)
   ```

2. **Belt Advancement View:**
   ```python
   @login_required
   def advance_belt(request):
       """
       Processa avanço de faixa se critérios forem atendidos.
       PRD linhas 362-388: Belt-based progression criteria
       """
       if request.method != 'POST':
           return redirect('progress:dashboard')
       
       user_progress = UserProgress.objects.get(user=request.user)
       
       if not user_progress.can_advance_to_next_belt():
           messages.error(request, 'Você ainda não atende os critérios para avançar de faixa.')
           return redirect('progress:dashboard')
       
       next_belt = BeltLevel.objects.filter(
           order=user_progress.current_belt.order + 1
       ).first()
       
       if not next_belt:
           messages.info(request, 'Você já está na faixa máxima!')
           return redirect('progress:dashboard')
       
       # Avançar faixa
       user_progress.current_belt = next_belt
       user_progress.save()
       
       messages.success(
           request, 
           f'Parabéns! Você avançou para a faixa {next_belt.get_color_display()}!'
       )
       return redirect('progress:dashboard')
   ```

**Referências do PRD:**
- Seção 3.1 (linhas 362-388): Belt progression criteria
- Seção 5.3 (linhas 492-522): Progress tracking and feedback

---

### 10. `apps/progress/urls.py`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
URL patterns para o app de progresso.

**O que fazer neste arquivo:**

```python
from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('dashboard/', views.progress_dashboard, name='dashboard'),
    path('advance-belt/', views.advance_belt, name='advance_belt'),
]
```

**Referências do PRD:**
- Seção 2.1 (linha 174): Progress app URL structure

---

### 11. `apps/audio/views.py`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
Serving de arquivos de áudio com headers apropriados e controle de acesso.

**O que fazer neste arquivo:**

1. **Audio Serving View:**
   ```python
   from django.shortcuts import get_object_or_404
   from django.http import FileResponse, Http404
   from django.contrib.auth.decorators import login_required
   from .models import AudioFile
   import os
   
   @login_required
   def serve_audio(request, audio_id):
       """
       Serve arquivo de áudio com headers apropriados.
       PRD: Secure audio delivery (linhas 228-268)
       
       Apenas usuários autenticados podem acessar áudio.
       """
       audio_file = get_object_or_404(AudioFile, id=audio_id)
       
       if not os.path.exists(audio_file.audio_file.path):
           raise Http404("Arquivo de áudio não encontrado")
       
       # Determinar content type baseado em extensão
       file_extension = os.path.splitext(audio_file.audio_file.name)[1].lower()
       content_type_map = {
           '.mp3': 'audio/mpeg',
           '.ogg': 'audio/ogg',
           '.opus': 'audio/opus',
       }
       content_type = content_type_map.get(file_extension, 'application/octet-stream')
       
       response = FileResponse(
           open(audio_file.audio_file.path, 'rb'),
           content_type=content_type
       )
       
       # Headers para caching (PRD linha 238)
       response['Cache-Control'] = 'public, max-age=31536000'  # 1 ano
       response['X-Content-Type-Options'] = 'nosniff'
       
       return response
   ```

**Referências do PRD:**
- Seção 2.3 (linhas 228-268): Audio handling and delivery
- Linha 180: Audio views for serving files

---

### 12. `apps/audio/urls.py`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
URL patterns para serving de áudio.

**O que fazer neste arquivo:**

```python
from django.urls import path
from . import views

app_name = 'audio'

urlpatterns = [
    path('<int:audio_id>/', views.serve_audio, name='serve_audio'),
]
```

**Referências do PRD:**
- Seção 2.1 (linha 180): Audio app structure

---

### 13. `templates/base.html`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
Template base HTML que serve como estrutura para todas as páginas do site.

**O que fazer neste arquivo:**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Coreano Marcial - Aprenda coreano para artes marciais">
    
    <!-- Security headers já configurados em settings.py CSP -->
    
    <title>{% block title %}Coreano Marcial{% endblock %}</title>
    
    <!-- CSS -->
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Header / Navigation -->
    <header>
        <nav>
            <a href="{% url 'lessons:home' %}">Início</a>
            
            {% if user.is_authenticated %}
                <a href="{% url 'lessons:belt_level_list' %}">Faixas</a>
                <a href="{% url 'progress:dashboard' %}">Meu Progresso</a>
                <a href="{% url 'logout' %}">Sair ({{ user.username }})</a>
            {% else %}
                <a href="{% url 'login' %}">Entrar</a>
            {% endif %}
        </nav>
    </header>
    
    <!-- Messages -->
    {% if messages %}
        <div class="messages">
            {% for message in messages %}
                <div class="message {{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        </div>
    {% endif %}
    
    <!-- Main Content -->
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    <footer>
        <p>&copy; 2026 Coreano Marcial</p>
    </footer>
    
    <!-- JavaScript -->
    {% block extra_js %}{% endblock %}
</body>
</html>
```

**Referências do PRD:**
- Seção 2.1 (linhas 166-173): Template structure
- Linha 13: Mobile-first design

---

### 14. `templates/lessons/home.html`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
Homepage do sistema - landing page pública.

**O que fazer neste arquivo:**

```html
{% extends 'base.html' %}

{% block title %}Início - Coreano Marcial{% endblock %}

{% block content %}
<section class="hero">
    <h1>Coreano Marcial</h1>
    <p>Aprenda coreano autêntico para artes marciais</p>
    <p>Metodologia audio-first • Sem romanização • Progressão por faixas</p>
    
    {% if not user.is_authenticated %}
        <a href="{% url 'login' %}" class="cta-button">Começar Agora</a>
    {% else %}
        <a href="{% url 'lessons:belt_level_list' %}" class="cta-button">Continuar Aprendendo</a>
    {% endif %}
</section>

<section class="features">
    <h2>Como Funciona</h2>
    
    <div class="feature">
        <h3>🎵 Audio-First</h3>
        <p>Aprenda pronúncia autêntica com falantes nativos. Nada de romanização.</p>
    </div>
    
    <div class="feature">
        <h3>🥋 Contexto de Artes Marciais</h3>
        <p>Vocabulário específico para dojang, comandos, cumprimentos e técnicas.</p>
    </div>
    
    <div class="feature">
        <h3>📊 Progressão por Faixas</h3>
        <p>Avance de faixa branca a preta conforme domina o conteúdo.</p>
    </div>
</section>

<section class="belt-preview">
    <h2>Faixas Disponíveis</h2>
    <div class="belt-grid">
        {% for belt in belt_levels %}
            <div class="belt-card" style="border-left: 5px solid {{ belt.color }}">
                <h3>{{ belt.get_color_display }}</h3>
                <p>{{ belt.korean_name }}</p>
                <p>{{ belt.description|truncatewords:15 }}</p>
            </div>
        {% endfor %}
    </div>
</section>
{% endblock %}
```

**Referências do PRD:**
- Linha 12: "Audio-first methodology, zero romanization dependence"
- Linha 914: Simple progression explanation

---

### 15. `templates/lessons/lesson_detail.html`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
Página de detalhe de uma lição específica com vocabulário.

**O que fazer neste arquivo:**

```html
{% extends 'base.html' %}

{% block title %}{{ lesson.title }} - Coreano Marcial{% endblock %}

{% block content %}
<div class="lesson-header">
    <span class="belt-indicator" style="background-color: {{ lesson.belt_level.color }}">
        {{ lesson.belt_level.get_color_display }}
    </span>
    
    <h1>{{ lesson.title }}</h1>
    <h2 class="korean-title">{{ lesson.title_korean }}</h2>
    
    <p>{{ lesson.description }}</p>
    
    {% if lesson_progress %}
        <div class="progress-badge">
            Status: {{ lesson_progress.get_status_display }}
        </div>
    {% endif %}
</div>

<section class="vocabulary-list">
    <h3>Vocabulário ({{ vocabulary_items.count }})</h3>
    
    {% for vocab in vocabulary_items %}
        <div class="vocab-card">
            <div class="vocab-korean">{{ vocab.korean_text }}</div>
            <div class="vocab-translation">{{ vocab.portuguese_translation }}</div>
            
            {% if vocab.martial_arts_context %}
                <div class="vocab-context">
                    <strong>Contexto:</strong> {{ vocab.martial_arts_context }}
                </div>
            {% endif %}
            
            {% if vocab.audio %}
                <audio controls preload="metadata">
                    <source src="{% url 'audio:serve_audio' vocab.audio.id %}" type="audio/mpeg">
                    Seu navegador não suporta áudio.
                </audio>
            {% else %}
                <p class="no-audio">Áudio não disponível</p>
            {% endif %}
        </div>
    {% empty %}
        <p>Nenhum vocabulário disponível nesta lição.</p>
    {% endfor %}
</section>

<div class="lesson-actions">
    <a href="{% url 'lessons:vocabulary_practice' lesson.id %}" class="button">
        Praticar Vocabulário
    </a>
    
    <a href="{% url 'lessons:lesson_list' lesson.belt_level.id %}" class="button-secondary">
        Voltar para Lições
    </a>
</div>
{% endblock %}
```

**Referências do PRD:**
- Linha 12: Zero romanization (apenas Hangul mostrado)
- Seção 2.3 (linhas 228-268): Audio playback
- Seção 5.2 (linhas 454-491): Lesson content presentation

---

### 16. `templates/progress/dashboard.html`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
Dashboard de progresso do usuário.

**O que fazer neste arquivo:**

```html
{% extends 'base.html' %}

{% block title %}Meu Progresso - Coreano Marcial{% endblock %}

{% block content %}
<h1>Meu Progresso</h1>

<section class="current-belt">
    <h2>Faixa Atual</h2>
    <div class="belt-display" style="background-color: {{ user_progress.current_belt.color }}">
        <h3>{{ user_progress.current_belt.get_color_display }}</h3>
        <p class="korean-name">{{ user_progress.current_belt.korean_name }}</p>
    </div>
</section>

<section class="statistics">
    <h2>Estatísticas</h2>
    
    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-number">{{ completed_lessons }}</div>
            <div class="stat-label">Lições Completadas</div>
        </div>
        
        <div class="stat-card">
            <div class="stat-number">{{ in_progress_lessons }}</div>
            <div class="stat-label">Lições em Progresso</div>
        </div>
        
        <div class="stat-card">
            <div class="stat-number">{{ mastered_vocab }}</div>
            <div class="stat-label">Vocabulário Dominado</div>
        </div>
        
        <div class="stat-card">
            <div class="stat-number">{{ user_progress.overall_accuracy }}%</div>
            <div class="stat-label">Acurácia Geral</div>
        </div>
    </div>
</section>

{% if next_belt %}
    <section class="next-belt">
        <h2>Próxima Faixa: {{ next_belt.get_color_display }}</h2>
        
        <div class="requirements">
            <h3>Requisitos:</h3>
            <ul>
                <li>
                    Lições completadas: {{ user_progress.total_lessons_completed }} / {{ next_belt.min_lessons_completed }}
                    {% if user_progress.total_lessons_completed >= next_belt.min_lessons_completed %}✅{% endif %}
                </li>
                <li>
                    Vocabulário dominado: {{ user_progress.total_vocabulary_mastered }} / {{ next_belt.min_vocabulary_mastered }}
                    {% if user_progress.total_vocabulary_mastered >= next_belt.min_vocabulary_mastered %}✅{% endif %}
                </li>
                <li>
                    Acurácia mínima: {{ user_progress.overall_accuracy }}% / {{ next_belt.min_accuracy_percentage }}%
                    {% if user_progress.overall_accuracy >= next_belt.min_accuracy_percentage %}✅{% endif %}
                </li>
            </ul>
        </div>
        
        {% if can_advance %}
            <form method="post" action="{% url 'progress:advance_belt' %}">
                {% csrf_token %}
                <button type="submit" class="button-primary">
                    Avançar para {{ next_belt.get_color_display }}!
                </button>
            </form>
        {% else %}
            <p class="info">Continue praticando para atender todos os requisitos.</p>
        {% endif %}
    </section>
{% else %}
    <section class="max-belt">
        <h2>🎉 Parabéns!</h2>
        <p>Você alcançou a faixa máxima!</p>
    </section>
{% endif %}

<section class="recent-activity">
    <h2>Atividade Recente</h2>
    <p>Última atividade: {{ user_progress.last_activity|date:"d/m/Y H:i" }}</p>
</section>
{% endblock %}
```

**Referências do PRD:**
- Seção 3.1 (linhas 362-388): Belt progression display
- Seção 5.3 (linhas 492-522): Progress feedback

---

### 17. `static/css/main.css`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
CSS principal do site. Mobile-first design.

**O que fazer neste arquivo:**

```css
/* Reset básico */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Mobile-first base styles */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
}

/* Navigation */
header nav {
    background-color: #2c3e50;
    padding: 1rem;
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

header nav a {
    color: white;
    text-decoration: none;
    padding: 0.5rem 1rem;
}

header nav a:hover {
    background-color: #34495e;
    border-radius: 4px;
}

/* Main content */
main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem;
}

/* Messages */
.messages {
    margin: 1rem 0;
}

.message {
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 4px;
}

.message.success {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
}

.message.error {
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
}

/* Korean text styling */
.korean-title,
.vocab-korean {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0.5rem 0;
}

/* Belt colors */
.belt-indicator,
.belt-display {
    padding: 0.5rem 1rem;
    border-radius: 4px;
    color: white;
    display: inline-block;
}

/* Cards */
.vocab-card,
.belt-card,
.stat-card {
    background: white;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Buttons */
.button,
.cta-button,
.button-primary {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background-color: #3498db;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    border: none;
    cursor: pointer;
    font-size: 1rem;
}

.button:hover,
.cta-button:hover,
.button-primary:hover {
    background-color: #2980b9;
}

.button-secondary {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background-color: #95a5a6;
    color: white;
    text-decoration: none;
    border-radius: 4px;
}

/* Audio player */
audio {
    width: 100%;
    margin-top: 0.5rem;
}

/* Responsive design - tablet and desktop */
@media (min-width: 768px) {
    .belt-grid,
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
    }
}

@media (min-width: 1024px) {
    .belt-grid,
    .stat-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

/* Footer */
footer {
    background-color: #2c3e50;
    color: white;
    text-align: center;
    padding: 2rem;
    margin-top: 4rem;
}
```

**Referências do PRD:**
- Linha 13: "Mobile-first"
- Seção 2.1 (linha 185): CSS structure

---

### 18. `requirements.txt`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
Dependências Python do projeto.

**O que fazer neste arquivo:**

```
# Django core
Django==5.0.1

# Database
psycopg2-binary==2.9.9  # PostgreSQL adapter

# Security
django-csp==3.8  # Content Security Policy headers

# Production server (opcional para desenvolvimento)
gunicorn==21.2.0

# Development tools
django-debug-toolbar==4.2.0  # Apenas para DEBUG=True

# Dependency audit (PRD linha 862)
pip-audit==2.7.0
```

**Referências do PRD:**
- Linha 188: requirements.txt
- Linha 862: "Dependency audit (pip-audit or Safety)"
- Seção 4.1: django-csp para CSP headers

---

### 19. `.env.example`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
Template de variáveis de ambiente. Não contém valores reais.

**O que fazer neste arquivo:**

```
# Django settings
DJANGO_SECRET_KEY=your-secret-key-here-generate-with-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=coreano_marcial
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Security (production only)
# HTTPS=True
# SECURE_SSL_REDIRECT=True
```

**Referências do PRD:**
- Seção 9 (linha 852): "SECRET_KEY in environment variable, not code"
- Seção 4.1: Environment-based configuration

---

### 20. `.gitignore`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
Arquivos que não devem ser versionados no Git.

**O que fazer neste arquivo:**

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
db.sqlite3
db.sqlite3-journal
/staticfiles/
/media/

# Environment variables
.env
.env.local

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Security - NEVER commit these
secret_key.txt
*.pem
*.key
```

**Referências do PRD:**
- Seção 9: Security checklist - nunca versionar SECRET_KEY
- Linha 852: SECRET_KEY protection

---

### 21. `manage.py`

**Tipo:** (X) Criar ( ) Modificar

**Responsabilidade do arquivo:**  
Script de gerenciamento Django padrão.

**O que fazer neste arquivo:**

```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
```

**Referências do PRD:**
- Padrão Django (linha 89): Django project structure

---

## Estrutura de Dados / Modelos

### Diagrama de Relacionamentos:

```
User (Django default)
  ├─ 1:1 → UserProfile
  └─ 1:1 → UserProgress
           └─ M:1 → BeltLevel

BeltLevel
  ├─ 1:M → Lesson
  └─ 1:M → UserProgress (current_belt)

Lesson
  ├─ 1:M → Vocabulary
  ├─ 1:M → LessonProgress
  └─ M:1 → BeltLevel

Vocabulary
  ├─ 1:1 → AudioFile
  ├─ 1:M → VocabularyMastery
  └─ M:1 → Lesson

LessonProgress
  ├─ M:1 → User
  └─ M:1 → Lesson

VocabularyMastery
  ├─ M:1 → User
  └─ M:1 → Vocabulary
```

### Campos Obrigatórios (não-null):

**BeltLevel:**
- name, color, order, korean_name, description
- min_lessons_completed, min_vocabulary_mastered, min_accuracy_percentage (com defaults)

**Lesson:**
- title, title_korean, belt_level, order, description, theme

**Vocabulary:**
- lesson, korean_text, portuguese_translation, order

**AudioFile:**
- vocabulary, audio_file

**UserProgress:**
- user, current_belt

**LessonProgress:**
- user, lesson, status

**VocabularyMastery:**
- user, vocabulary, mastery_level

### Constraints:

- `unique_together`: (belt_level, order) em Lesson
- `unique_together`: (lesson, order) em Vocabulary
- `unique_together`: (user, lesson) em LessonProgress
- `unique_together`: (user, vocabulary) em VocabularyMastery
- `OneToOneField`: User ↔ UserProfile, User ↔ UserProgress, Vocabulary ↔ AudioFile

---

## Fluxo de Execução

### 1. Registro e Autenticação do Usuário:

1. Usuário acessa homepage (`/`)
2. Clica em "Começar Agora" → redireciona para `/accounts/login/`
3. Django auth views gerenciam login/registro
4. Após autenticação, signal `post_save` cria automaticamente:
   - `UserProfile` (via signal em `apps/users/models.py`)
   - `UserProgress` com `current_belt` = BeltLevel.objects.first() (Faixa Branca)
5. Redirecionamento para `/belts/` (lista de faixas)

### 2. Navegação por Faixas e Lições:

1. Usuário em `/belts/` vê todas as faixas disponíveis
2. Clica em uma faixa → `/belts/<belt_id>/lessons/`
3. Vê lista de lições daquela faixa com indicador de progresso (não iniciada/em progresso/completada)
4. Clica em uma lição → `/lessons/<lesson_id>/`
5. View `lesson_detail`:
   - Verifica se `LessonProgress` existe
   - Se não existir ou status == 'not_started':
     - Cria/atualiza `LessonProgress` com status='in_progress', started_at=now()
   - Renderiza template com vocabulário e áudio

### 3. Estudo de Vocabulário:

1. Na página da lição, usuário vê lista de vocabulário
2. Cada item mostra:
   - `korean_text` (Hangul, SEM romanização)
   - `portuguese_translation`
   - `martial_arts_context` (se disponível)
   - Player de áudio HTML5 (`<audio controls>`)
3. Usuário clica em play do áudio:
   - Request para `/audio/<audio_id>/`
   - View `serve_audio` verifica autenticação
   - Retorna FileResponse com headers de cache
4. FASE 0: Não há tracking de "ouviu áudio" ou "marcou como dominado" - isso virá em fases futuras

### 4. Prática de Vocabulário:

1. Usuário clica em "Praticar Vocabulário" → `/lessons/<lesson_id>/practice/`
2. FASE 0: View renderiza template simples com todos os vocabulários da lição
3. Usuário pode ouvir áudio de cada item
4. NÃO há quiz ou assessment nesta fase
5. Pronunciation assessment será adicionado na Fase 3 (fora desta SPEC)

### 5. Completar Lição:

1. FASE 0: Não há botão "Completar Lição" automático
2. Usuário deve marcar manualmente (admin) ou será implementado em iterações futuras
3. Quando `LessonProgress.status` = 'completed':
   - `UserProgress.total_lessons_completed` é incrementado
   - Isso afeta critérios de avanço de faixa

### 6. Avanço de Faixa:

1. Usuário acessa `/progress/dashboard/`
2. View `progress_dashboard` mostra:
   - Faixa atual
   - Estatísticas (lições completadas, vocabulário dominado, acurácia)
   - Próxima faixa e requisitos
   - Botão "Avançar" se `can_advance_to_next_belt()` retornar True
3. Usuário clica em "Avançar para [próxima faixa]":
   - POST request para `/progress/advance-belt/`
   - View verifica critérios novamente (segurança)
   - Se OK: atualiza `UserProgress.current_belt` para próxima faixa
   - Exibe mensagem de sucesso
   - Redireciona de volta para dashboard

---

## Segurança e Restrições

### Riscos Identificados no PRD e Mitigações:

**1. Service Worker Vulnerabilities (PRD linhas 193-226):**
- **Mitigação FASE 0:** Service Worker NÃO será implementado nesta spec (apenas Fase 2)
- **Preparação:** CSP headers já configurados em settings.py para quando Service Worker for adicionado

**2. CSRF Attacks (PRD linhas 141-151, linha 854):**
- **Mitigação:**
  - Django CSRF middleware ATIVO (settings.py)
  - `{% csrf_token %}` em todos os forms (ex: `advance_belt` form)
  - CSRF cookies com Secure, HttpOnly, SameSite=Strict

**3. XSS (Cross-Site Scripting):**
- **Mitigação:**
  - Django auto-escaping de templates (padrão)
  - CSP headers bloqueiam scripts inline não autorizados
  - Validação de user input (Django forms, quando implementados)

**4. SQL Injection (PRD linha 859):**
- **Mitigação:**
  - Django ORM (nenhuma raw query nesta SPEC)
  - Se raw queries forem necessárias no futuro: usar parameterized queries

**5. File Upload Vulnerabilities (PRD linha 860):**
- **Mitigação:**
  - FASE 0: Apenas admin pode fazer upload de áudio
  - `FileExtensionValidator` em `AudioFile.audio_file` permite apenas .mp3, .ogg, .opus
  - Serving via view com autenticação (`@login_required`)
  - Se user uploads forem permitidos no futuro: adicionar validação de MIME type, antivirus scan

**6. Session Hijacking:**
- **Mitigação:**
  - Session cookies: Secure=True, HttpOnly=True, SameSite=Strict (settings.py)
  - HTTPS enforced em produção (PRD linha 850)

**7. Sensitive Data Exposure (PRD linha 852):**
- **Mitigação:**
  - SECRET_KEY em variável de ambiente (.env)
  - DEBUG=False em produção
  - .gitignore protege .env, *.log, db.sqlite3

**8. Audio File Size DoS (PRD linhas 70, 825):**
- **Mitigação FASE 0:** Apenas admin faz upload
- **Preparação:** FileField aceita validação de tamanho (MaxSizeValidator) - implementar se necessário

### O que NÃO pode ser feito na implementação:

1. ❌ NÃO adicionar Service Worker (reservado para Fase 2)
2. ❌ NÃO adicionar HTMX (reservado para Fase 1)
3. ❌ NÃO adicionar Pronunciation Assessment API (reservado para Fase 3)
4. ❌ NÃO adicionar romanização em NENHUM lugar (decisão pedagógica firme do PRD)
5. ❌ NÃO permitir user uploads de áudio nesta fase
6. ❌ NÃO desabilitar CSRF protection
7. ❌ NÃO commitar SECRET_KEY ou .env no Git
8. ❌ NÃO usar DEBUG=True em produção
9. ❌ NÃO usar HTTP (apenas HTTPS em produção)
10. ❌ NÃO adicionar funcionalidades de gamification não especificadas (pontos, streaks, leaderboards)

---

## Dependências

### Bibliotecas Python (requirements.txt):

1. **Django==5.0.1** - Framework web principal
2. **psycopg2-binary==2.9.9** - PostgreSQL database adapter
3. **django-csp==3.8** - Content Security Policy headers
4. **gunicorn==21.2.0** - Production WSGI server
5. **django-debug-toolbar==4.2.0** - Development debugging (apenas DEBUG=True)
6. **pip-audit==2.7.0** - Security audit de dependências

### Configurações Necessárias:

**Variáveis de Ambiente (.env):**
- `DJANGO_SECRET_KEY` (obrigatório, gerar com `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG` (True para desenvolvimento, False para produção)
- `ALLOWED_HOSTS` (comma-separated, ex: `localhost,127.0.0.1`)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` (PostgreSQL)

**Banco de Dados:**
- PostgreSQL 12+ (recomendado)
- Criar database: `CREATE DATABASE coreano_marcial;`
- Migrations: `python manage.py migrate`

**Diretórios a Criar:**
```
mkdir -p media/audio
mkdir -p static/css
mkdir -p logs
```

**Comandos de Setup:**
```bash
# Criar virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Copiar .env.example para .env e preencher valores
cp .env.example .env

# Criar database
createdb coreano_marcial

# Migrations
python manage.py makemigrations
python manage.py migrate

# Criar superuser para admin
python manage.py createsuperuser

# Coletar static files (produção)
python manage.py collectstatic

# Rodar servidor de desenvolvimento
python manage.py runserver
```

### Flags ou Feature Toggles:

**FASE 0:** Nenhuma feature flag necessária.

**Preparação para Fases Futuras:**
- Quando implementar HTMX (Fase 1): adicionar `django-htmx` ao requirements.txt
- Quando implementar PWA (Fase 2): adicionar Service Worker JS, manifest.json
- Quando implementar Pronunciation API (Fase 3): adicionar bibliotecas de API client conforme escolha (Azure SDK, Speechace, etc)

---

## Critérios de Aceitação

Esta SPEC será considerada correta se e somente se:

### 1. Estrutura de Arquivos:

- [ ] Todos os arquivos listados nesta SPEC foram criados
- [ ] Nenhum arquivo não listado foi criado sem justificativa
- [ ] Estrutura de diretórios segue exatamente o layout especificado:
  ```
  project_root/
  ├── config/
  │   ├── settings.py
  │   ├── urls.py
  │   └── wsgi.py
  ├── apps/
  │   ├── lessons/
  │   ├── progress/
  │   ├── audio/
  │   └── users/
  ├── templates/
  ├── static/
  ├── media/
  ├── logs/
  ├── manage.py
  ├── requirements.txt
  ├── .env.example
  └── .gitignore
  ```

### 2. Modelos de Dados:

- [ ] Todos os modelos especificados (`BeltLevel`, `Lesson`, `Vocabulary`, `AudioFile`, `UserProfile`, `UserProgress`, `LessonProgress`, `VocabularyMastery`) foram criados
- [ ] Campos obrigatórios estão presentes com tipos corretos
- [ ] Constraints (`unique_together`, `OneToOneField`) implementados
- [ ] Relacionamentos (ForeignKey, OneToOne) corretos
- [ ] Migrations rodam sem erro: `python manage.py migrate`
- [ ] Admin pode criar registros via Django Admin

### 3. Views e URLs:

- [ ] Todas as views especificadas foram implementadas
- [ ] URLs mapeadas corretamente
- [ ] Decorators `@login_required` aplicados onde especificado
- [ ] Views retornam status HTTP correto (200 para sucesso, 404 para not found)

### 4. Templates:

- [ ] `base.html` existe e funciona como template base
- [ ] Templates de lições (`home.html`, `lesson_detail.html`) herdam de `base.html`
- [ ] Template de progresso (`dashboard.html`) renderiza corretamente
- [ ] Nenhuma romanização aparece em templates (apenas Hangul)
- [ ] `{% csrf_token %}` presente em todos os forms POST

### 5. Segurança:

- [ ] `DEBUG=False` funciona sem erros em settings.py
- [ ] `SECRET_KEY` vem de variável de ambiente
- [ ] `ALLOWED_HOSTS` configurado corretamente
- [ ] CSRF middleware ativo
- [ ] CSP headers configurados (`django-csp` instalado)
- [ ] Session cookies: Secure, HttpOnly, SameSite=Strict
- [ ] `.env` em `.gitignore`
- [ ] Nenhum secret commitado no Git

### 6. Áudio:

- [ ] `AudioFile` model aceita apenas .mp3, .ogg, .opus
- [ ] View `serve_audio` requer autenticação
- [ ] Arquivos de áudio servidos com headers corretos (Content-Type, Cache-Control)
- [ ] Upload de áudio via admin funciona

### 7. Progressão:

- [ ] `UserProgress` criado automaticamente ao criar User
- [ ] `current_belt` inicializa com primeira faixa (Branca)
- [ ] Método `can_advance_to_next_belt()` funciona corretamente
- [ ] View `advance_belt` valida critérios antes de avançar
- [ ] Dashboard mostra estatísticas corretas

### 8. Nenhuma Funcionalidade Extra:

- [ ] HTMX NÃO está presente (Fase 1)
- [ ] Service Worker NÃO existe (Fase 2)
- [ ] Pronunciation API NÃO integrado (Fase 3)
- [ ] Nenhuma romanização adicionada
- [ ] Nenhum gamification (pontos, streaks) implementado

### 9. Testes Manuais Passam:

- [ ] Usuário consegue se registrar e fazer login
- [ ] Usuário consegue ver lista de faixas
- [ ] Usuário consegue ver lições de uma faixa
- [ ] Usuário consegue abrir detalhe de uma lição
- [ ] Áudio player funciona (requer áudio no banco via admin)
- [ ] Dashboard de progresso mostra dados corretos
- [ ] Usuário pode avançar de faixa quando critérios são atendidos

### 10. Código Limpo:

- [ ] Nenhum código comentado desnecessário
- [ ] Nenhum `print()` de debug esquecido
- [ ] Nenhum import não utilizado
- [ ] Docstrings presentes em modelos e views principais
- [ ] Código segue PEP 8 (Python style guide)

---

## Fora de Escopo

**Qualquer funcionalidade não descrita explicitamente nesta SPEC não deve ser implementada.**

Especificamente, está FORA DO ESCOPO desta SPEC:

### Fase 1 (HTMX - Futuro):
- Integração HTMX
- Views duplicadas (full page + fragments)
- Templates parciais (_partials/)
- Headers `HX-Request` checking

### Fase 2 (PWA - Futuro):
- Service Worker (`service-worker.js`)
- PWA Manifest (`manifest.json`)
- Offline caching
- Background sync
- Cache management strategies
- IndexedDB para offline data

### Fase 3 (Pronunciation API - Futuro):
- Azure Pronunciation Assessment integration
- Speechace API integration
- SpeechSuper API integration
- Microphone access
- Audio recording no browser
- Pronunciation scoring
- Feedback de pronúncia

### Funcionalidades Não Planejadas:
- Gamification (pontos, badges, streaks, leaderboards)
- Social features (amigos, competição, compartilhamento)
- Chat/messaging
- Notificações push
- Multi-idioma (apenas PT-BR e Coreano)
- CMS para conteúdo (usar Django Admin)
- Analytics tracking (Google Analytics, etc)
- A/B testing
- Payment integration
- Subscription system
- Certificados de conclusão
- Exportação de progresso (PDF reports)
- Mobile apps nativos (apenas PWA no futuro)

### Otimizações Não Prioritárias:
- CDN para static files (pode usar Cloudflare na produção, mas não é parte da SPEC)
- Redis para caching
- Celery para tarefas assíncronas
- ElasticSearch para busca
- GraphQL API
- WebSockets para real-time features

---

## Observações Finais

### Limitações Conhecidas (Fase 0):

1. **Nenhuma interatividade HTMX:** Todas as páginas recarregam completamente. Isso é intencional para Fase 0.

2. **Nenhum modo offline:** PWA será adicionado na Fase 2. Usuários precisam estar online.

3. **Nenhum assessment de pronúncia:** Usuários podem apenas ouvir áudio. Assessment vem na Fase 3.

4. **Content gerenciado via Django Admin:** Não há CMS dedicado. Professores/administradores usam `/admin/` para adicionar lições, vocabulário, áudio.

5. **Estatísticas de progresso básicas:** `VocabularyMastery` existe no modelo mas não há interface para usuário marcar "dominei este vocabulário". Isso será adicionado em iterações futuras.

6. **Nenhum quiz ou exercício:** Fase 0 é apenas apresentação de conteúdo (lições, vocabulário, áudio) e tracking de completude de lições.

### Pontos para Versões Futuras:

**Fase 1 (Next Iteration):**
- Adicionar HTMX para partial updates (menos reloads de página)
- Refatorar views para retornar fragments quando `HX-Request` header presente
- Criar templates parciais em `_fragments/`

**Fase 2:**
- Implementar Service Worker com segurança (PRD linhas 193-226)
- PWA Manifest
- Estratégia de cache (stale-while-revalidate para HTML, cache-first para áudio)
- Background sync para progresso offline

**Fase 3:**
- Integrar pronunciation assessment API
- UI para gravação de áudio
- Feedback visual de pronúncia
- Thresholds configuráveis (PRD linha 823)

**Melhorias de Conteúdo:**
- Adicionar mais lições (além das 20 iniciais)
- Expandir para outras artes marciais (PRD linha 890: "Korean for Physical Activities")
- Módulo de Hangul primer (PRD linha 832)

**Melhorias de UX:**
- Spaced repetition algorithm para vocabulário
- Modo de revisão (review mode)
- Pesquisa de vocabulário
- Favoritos/bookmarks
- Notas pessoais do usuário

### Ambiguidades Identificadas no PRD:

**1. Critérios exatos de avanço de faixa:**
- PRD menciona "min_lessons_completed, min_vocabulary_mastered, min_accuracy_percentage" (linha 369)
- SPEC implementa esses campos em `BeltLevel` e método `can_advance_to_next_belt()`
- **Ambiguidade:** O que conta como "vocabulary mastered"? 
  - **Resolução nesta SPEC:** `VocabularyMastery.mastery_level >= 4` (Proficiente ou Mestre)
  - **Nota:** Isso pode precisar ajuste após feedback de usuários

**2. Como marcar lição como "completada":**
- PRD não especifica critério exato
- **Resolução nesta SPEC:** Fase 0 NÃO implementa auto-completion. Isso será definido em iterações futuras. Possíveis critérios:
  - Usuário viu todo vocabulário
  - Usuário praticou X vezes
  - Usuário acertou quiz (quando implementado)
  - Usuário clica manualmente "completar lição"

**3. Acurácia geral (overall_accuracy) em `UserProgress`:**
- Como calcular sem pronunciation assessment na Fase 0?
- **Resolução nesta SPEC:** Campo existe no modelo mas ficará em 0.0 até Fase 3. Quando pronunciation API for integrado, será calculado como média de acertos em assessments.

**4. Audio file size limits:**
- PRD menciona "1-5MB per file" (linha 70) e storage quotas (linha 71)
- **Resolução nesta SPEC:** Nenhum limite programático implementado na Fase 0. Admin é responsável por fazer upload de arquivos razoáveis.
- **Recomendação para futuro:** Adicionar `MaxSizeValidator(5*1024*1024)` ao `AudioFile.audio_file` field.

### Warnings Importantes:

⚠️ **CSRF Token:** Certifique-se que TODOS os forms POST incluem `{% csrf_token %}`. Falha nisso causará 403 Forbidden.

⚠️ **Migrations:** Sempre rodar `python manage.py makemigrations` após criar/modificar models, ANTES de `migrate`.

⚠️ **Static Files:** Em produção, rodar `python manage.py collectstatic` antes de deploy.

⚠️ **SECRET_KEY:** NUNCA commitar `.env` no Git. Sempre usar `.env.example` como template.

⚠️ **PostgreSQL:** Certifique-se que PostgreSQL está rodando antes de `migrate`. Se usar SQLite em desenvolvimento, trocar para PostgreSQL ANTES de produção (migrações podem ter problemas).

⚠️ **HTTPS:** Em produção, HTTPS é OBRIGATÓRIO (PRD linha 850). Usar Let's Encrypt para certificado gratuito.

⚠️ **Audio Storage:** Em produção, considerar usar S3/Cloudflare R2 para servir arquivos de áudio (PRD linha 792). Fase 0 usa filesystem local (MEDIA_ROOT).

---

**Status da SPEC:** ✅ Completa e pronta para implementação (Fase 0 apenas)  
**Próximo Passo:** Implementar EXATAMENTE o que está descrito aqui, sem adicionar funcionalidades extras.  
**Revisão Necessária:** Antes de iniciar Fase 1, revisar esta SPEC e atualizar conforme aprendizados da Fase 0.
