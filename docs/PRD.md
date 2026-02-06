# Product Research Document (PRD)
## Coreano Marcial - Korean Language Learning for Martial Arts

**Version:** 1.0  
**Date:** January 27, 2026  
**Document Type:** Critical Technical Validation & Risk Assessment
**Ratified:** 2026-02-06
**Ratified By:** Maintainer + Designated Reviewer
**Change Summary:** Canonical PRD ratified with governance alignment, constitution mapping, and phased delivery guardrails.

---


## Constitution Compliance

This PRD is the canonical product document and is governed by `.specify/memory/constitution.md`.

- **Alignment:** Scope, phase planning, and security constraints are explicitly documented before implementation work starts.
- **Governance:** PRD/spec updates must include `Constitution Compliance`, `Sync Impact Report`, and a named Designated Reviewer in PRs.
- **Security/Privacy:** Any PRD/security-impacting change requires corresponding update in `docs/threats_v_0.md` and explicit security review before merge.

---

## Executive Summary

**Project Vision:** A server-driven Progressive Web Application (PWA) for teaching Korean language specifically contextualized to martial arts terminology, with emphasis on authentic pronunciation through audio-first methodology, zero romanization dependence, and hierarchical progression modeling traditional martial arts belt systems.

**Stack:** Django + HTMX + PWA  
**Target:** Mobile-first, offline-capable educational platform  
**Non-negotiables:** Documentation, Security (AppSec/DevSecOps), No heavy frontend frameworks

### Critical Assessment Summary

**Viability:** ⚠️ **Technically feasible but high-risk**  
**Innovation:** Niche does not exist in this exact form (Korean + Martial Arts learning apps exist separately)  
**Complexity:** Medium-to-High (deceptively simple concept masks implementation challenges)  
**Maintenance Burden:** High (audio content, multiple systems, offline sync)

---

## 1. Market & Concept Validation

### 1.1 Existing Solutions Analysis

#### Similar Projects Found:

**TKDojang (2024)** - iOS Taekwondo learning app
- Features: Korean terminology, offline-first, multi-profile
- Limitations: Mobile-only, vocabulary games focus, no pronunciation assessment
- Stack: Native iOS
- Key insight: Market exists but is underserved

**Martial Arts + Korean Resources** (Web)
- Black Belt Wiki, TaekwondoNation.com - Static terminology lists
- No interactivity, no pronunciation guidance
- Purely reference material

**General Korean Learning Apps:**
- **Teuida, ELSA, Speechling** - Focus on pronunciation with AI feedback
- **Drops, LingoDeer** - Vocabulary with optional romanization toggle
- **None** combine martial arts context with systematic Korean learning

#### Critical Gap Identified:
✅ No comprehensive martial arts-focused Korean learning platform exists  
⚠️ BUT: The intersection is narrow - potential user base is small (martial artists serious about Korean language study)

## Product Requirements (canonical)

### Purpose
Coreano Marcial é uma plataforma educacional focada no ensino progressivo de coreano aplicado ao contexto marcial.

Ela existe para resolver um problema específico: estudantes de artes marciais que desejam aprender coreano enfrentam conteúdo genérico, descontextualizado e pouco estruturado para seu objetivo real.

O projeto nasce para:

- Ensinar vocabulário funcional e contextualizado
- Organizar progressão de aprendizado clara
- Transformar estudo em prática consistente
- Integrar disciplina marcial com disciplina linguística

O foco não é aprender “coreano geral”. É aprender o coreano que faz sentido dentro da jornada marcial.

### Problem Statement
Atualmente:

- Conteúdo de coreano é amplo demais
- Falta contextualização para praticantes marciais
- Falta progressão estruturada focada em comandos, termos e cultura marcial
- O aprendizado depende excessivamente de motivação externa

Isso gera abandono, frustração e aprendizado fragmentado.

### Target Audience
O público-alvo é:

- Praticantes de artes marciais coreanas (hapkido, taekwondo, etc.)
- Estudantes autodidatas interessados na cultura marcial coreana
- Pessoas disciplinadas que valorizam progressão e estrutura

O projeto não é para consumo casual. É para quem valoriza constância e evolução.

### Core Value Proposition
Coreano Marcial oferece:

- Progressão estruturada por níveis
- Sistema de gamificação alinhado à disciplina marcial
- Aprendizado contextualizado (comandos, termos técnicos, cultura)
- Clareza de avanço e conquistas

Ele transforma estudo em jornada estruturada. Não é só conteúdo. É sistema de progressão.

### Core Principles
- Progressão clara — O usuário sempre sabe onde está e qual é o próximo passo.
- Contextualização marcial — Cada termo tem propósito dentro da prática.
- Disciplina como mecânica — A estrutura incentiva consistência.
- Simplicidade funcional — A experiência deve ser direta e sem distrações supérfluas.

### Scope Definition
**Inclui:**

- Módulos de aprendizado organizados por nível
- Sistema de progressão
- Feedback de evolução
- Elementos de gamificação coerentes com o domínio

**Não inclui:**

- Ensino completo de coreano geral
- Rede social ampla
- Funcionalidades não relacionadas ao aprendizado marcial

### Long-Term Vision
No longo prazo, o projeto pode se tornar:

- Referência em aprendizado linguístico aplicado a contexto específico
- Plataforma de ensino modular adaptável
- Base para expansão para outros contextos disciplinares

Mas o núcleo permanece: Ensino estruturado de coreano aplicado ao universo marcial.

### 1.2 What Typically Fails in This Space

Based on research into language learning apps and niche educational platforms:

**1. Content Maintenance Hell**
- Audio files require native speaker recordings
- Terminology standardization across martial arts styles (WTF vs ITF Taekwondo, different Hapkido schools)
- Updates when terminology evolves

**2. Pronunciation Assessment Reality**
- AI pronunciation scoring has 20-30% error rates for non-English languages
- Azure Pronunciation Assessment (Microsoft): "Performance varies depending on real-world use", requires clean audio
- Background noise severely degrades accuracy
- Multi-speaker scenarios not supported
- False positives/negatives demotivate learners

**3. Offline Sync Complexity**
- Audio files are large (1-5MB per high-quality pronunciation clip)
- PWA storage quotas vary by browser (Chrome: ~60% of disk space, Safari: 50MB initially)
- Service Worker cache management becomes exponentially complex
- Sync conflicts when users progress offline then reconnect

**4. Pedagogical Assumptions**
- Gamification often backfires (shallow engagement)
- Belt-based progression may not align with actual learning pace
- Zero romanization is linguistically correct but creates steep learning curve

**5. Abandonment Patterns**
- Language learning apps have ~90-day retention cliff
- Niche apps (martial arts) compound this with smaller initial user base
- Without social/competitive features, solo practice apps struggle

---

## 2. Architecture Deep Dive

### 2.1 Django + HTMX for Server-Driven SPA

#### Pattern Overview:
```
Browser Request → Django View → HTML Fragment → HTMX Swap → Partial DOM Update
```

#### What Research Shows:

**Advantages Validated:**
- Reduces frontend complexity (14KB HTMX vs 100KB+ React)
- Leverages Django's mature security (CSRF, XSS protections built-in)
- Single-team development (no frontend/backend split)
- SEO-friendly by default

**Critical Warnings from Production Use:**

From Medium article by Eddy-OJB (2024):
> "An annoying feature is that when I went to display a graph and change data dynamically, I had to replace the graph entirely instead of only updating the data."

From TestDriven.io Django+HTMX course:
> "HTMX requires a lot more views and, consequently, URLs and templates — you can't just dump them in one file and expect to be able to find or understand anything."

**Code Organization Challenge:**
```
Traditional Django:
- 10 views
- 10 URLs
- 15 templates

Django + HTMX:
- 40+ views (full page + fragments)
- 40+ URLs
- 60+ templates (base + partials)
```

#### Recommended Pattern (from django-htmx tutorial):

```python
# views.py
from django.shortcuts import render

def lesson_view(request):
    # Check if request is from HTMX
    if request.headers.get('HX-Request'):
        # Return only the content fragment
        return render(request, 'lessons/_content.html', context)
    else:
        # Return full page
        return render(request, 'lessons/lesson_page.html', context)
```

#### CSRF Token Handling (Critical for Security):

From Web With Django guide:
```html
<!-- base.html -->
<body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
    <!-- All HTMX requests will include CSRF token -->
</body>
```

**Risk:** If CSRF tokens are not properly configured in HTMX headers, ALL POST requests will fail silently or expose security vulnerabilities.

#### Files Impacted in Django Project:

```
project_root/
├── config/
│   ├── settings.py          # HTMX middleware, CORS, CSP headers
│   ├── urls.py              # Main URL routing
│   └── wsgi.py
├── apps/
│   ├── lessons/
│   │   ├── views.py         # 30+ views (full + fragments)
│   │   ├── urls.py          # Parallel URL patterns
│   │   ├── models.py
│   │   ├── templates/
│   │   │   ├── lessons/
│   │   │   │   ├── base.html
│   │   │   │   ├── lesson_list.html
│   │   │   │   └── _fragments/
│   │   │   │       ├── _lesson_card.html
│   │   │   │       ├── _progress_bar.html
│   │   │   │       └── _audio_player.html
│   ├── progress/
│   │   ├── views.py
│   │   ├── models.py        # User progress, belt levels
│   │   └── templates/
│   ├── audio/
│   │   ├── views.py         # Audio serving, transcoding
│   │   ├── models.py        # Audio metadata
│   │   └── storage/         # Audio file management
├── static/
│   ├── htmx.min.js          # 14KB
│   ├── alpine.min.js        # Optional: 15KB for client-side interactivity
│   └── css/
├── service-worker.js        # PWA offline logic
├── manifest.json            # PWA configuration
└── requirements.txt
```

### 2.2 PWA Implementation Risks

#### Service Worker Security Concerns:

From Koombea PWA Security Analysis:
> "Service workers are an attractive attack vector because they give bad actors ability to intercept connections or serve modified responses. If a cyber attacker gains control of a service worker, they can persistently attack inbound and outbound information."

From Progressive Web Apps Security Best Practices:
> "A compromised service worker can intercept network requests, manipulate cached data, or inject malicious scripts."

**Mitigation Requirements:**
```javascript
// service-worker.js - Secure implementation pattern
const CACHE_VERSION = 'v1.0.0';
const ALLOWED_ORIGINS = ['https://yourdomain.com']; // Whitelist

self.addEventListener('fetch', (event) => {
    // Validate origin
    const url = new URL(event.request.url);
    if (!ALLOWED_ORIGINS.includes(url.origin)) {
        return; // Don't intercept cross-origin requests
    }
    
    // Only cache GET requests
    if (event.request.method !== 'GET') {
        return;
    }
    
    event.respondWith(
        caches.match(event.request).then(cached => {
            return cached || fetch(event.request);
        })
    );
});
```

#### Audio Storage Reality Check:

**Storage Quota per Browser:**
- Chrome: Dynamic (~60% of available disk space)
- Firefox: 2GB hard limit
- Safari: 50MB initial, requires permission for more
- Edge: Similar to Chrome

**For 100 Korean phrases with quality audio:**
- High quality (192kbps MP3): ~3MB each = 300MB total
- Compressed (64kbps MP3): ~1MB each = 100MB total
- Opus/WebM: ~500KB each = 50MB total

**Problem:** Safari's 50MB limit is exceeded with quality audio. Users on iOS will have degraded experience or need to request storage permission.

#### Offline Sync Patterns:

From MDN PWA Documentation:
```javascript
// Background Sync API (not supported in Safari)
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-progress') {
        event.waitUntil(syncUserProgress());
    }
});

// Fallback: Manual sync on reconnection
window.addEventListener('online', () => {
    syncPendingData();
});
```

**Risk:** Background Sync API has poor browser support. Safari doesn't support it at all. Your PWA will need manual sync triggers, complicating UX.

### 2.3 Audio Implementation

#### Web Audio API vs HTML5 Audio Element:

**For pronunciation learning:**
```html
<!-- Simple approach: HTML5 Audio -->
<audio id="pronunciation" preload="metadata">
    <source src="/audio/annyeonghaseyo.opus" type="audio/ogg; codecs=opus">
    <source src="/audio/annyeonghaseyo.mp3" type="audio/mpeg">
</audio>

<button hx-get="/play-audio/phrase-123" hx-trigger="click">
    Play Pronunciation
</button>
```

**Problem:** HTMX doesn't handle media elements elegantly. You'll need JavaScript:
```javascript
// audio-handler.js
document.body.addEventListener('htmx:afterSwap', (event) => {
    const audio = document.getElementById('pronunciation');
    if (audio) {
        audio.play();
    }
});
```

#### Pronunciation Assessment - Third-Party API Required:

**Browser Web Speech API** (free but inaccurate):
- Chrome/Edge only
- No pronunciation scoring, just transcription
- Cannot assess Korean pronunciation quality

**Commercial APIs:**
- **Azure Pronunciation Assessment:** $1-4 per 1000 requests, only supports scripted speech
- **Speechace:** Pronunciation scoring, but primary focus on English (Korean support unclear)
- **ELSA API:** English-only
- **SpeechSuper:** Supports 8 languages including Korean, pricing undisclosed

**Critical Limitation:** All pronunciation APIs require:
- Clean audio (background noise degrades accuracy by 30-50%)
- Single speaker
- Normal speaking volume/speed
- Network connection (no offline assessment)

From Microsoft Azure documentation:
> "Noisy environments or multiple people speaking at the same time might lead to lower confidence of evaluation... Pronunciation Assessment's performance will vary depending on real-world use."

**Realistic Expectation:** Pronunciation assessment will have false positives/negatives. You'll need:
- Clear UX communicating limitations
- Manual review option
- Tolerance thresholds to avoid demotivating learners

---

## 3. Security Analysis (OWASP Focus)

### 3.1 OWASP Top 10 Risks for This Project

#### A01:2021 - Broken Access Control

**Risk in Coreano Marcial:**
- Users accessing belt levels they haven't unlocked
- Viewing other users' progress
- Modifying progress data via API manipulation

**Django Mitigation:**
```python
# lessons/views.py
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

@login_required
def belt_lesson(request, belt_level):
    user_belt = request.user.profile.current_belt
    if belt_level > user_belt:
        raise PermissionDenied("Belt level not yet unlocked")
    # ... return lesson
```

#### A02:2021 - Cryptographic Failures

**Risk:**
- Audio files cached in PWA contain copyrighted content
- User progress data stored without encryption
- Session tokens in localStorage (bad practice)

**Mitigation:**
```python
# settings.py
SESSION_COOKIE_SECURE = True  # HTTPS only
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
SESSION_COOKIE_SAMESITE = 'Strict'  # CSRF protection

# Encrypt sensitive data at rest
from django.db import models
from django_cryptography.fields import encrypt

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = encrypt(models.TextField())  # Private study notes
```

#### A03:2021 - Injection Attacks

**Risk in HTMX context:**
- User input in search queries injected into SQL
- Korean text input containing HTML/JavaScript

**Django Protection (built-in):**
```python
# views.py
from django.db.models import Q

def search_lessons(request):
    query = request.GET.get('q', '')
    # Django ORM prevents SQL injection by default
    results = Lesson.objects.filter(
        Q(korean_term__icontains=query) | Q(translation__icontains=query)
    )
    return render(request, '_search_results.html', {'results': results})
```

```html
<!-- templates/_search_results.html -->
{% for lesson in results %}
    <!-- Django template auto-escapes, prevents XSS -->
    <div>{{ lesson.korean_term }} - {{ lesson.translation }}</div>
{% endfor %}
```

#### A05:2021 - Security Misconfiguration

**Common PWA Pitfalls:**

```python
# settings.py - WRONG (Insecure defaults)
DEBUG = True  # NEVER in production
ALLOWED_HOSTS = ['*']  # Too permissive
CORS_ALLOW_ALL_ORIGINS = True  # Dangerous

# CORRECT
DEBUG = False
ALLOWED_HOSTS = ['coreano-marcial.com', 'www.coreano-marcial.com']
CORS_ALLOWED_ORIGINS = [
    'https://coreano-marcial.com',
]

# Content Security Policy (prevents XSS)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")  # HTMX requires inline
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_MEDIA_SRC = ("'self'", "blob:")  # For audio
```

#### A07:2021 - Identification and Authentication Failures

**Educational App Specific:**
- Users sharing accounts (family members)
- Weak password recovery
- No rate limiting on login attempts

**Required Implementation:**
```python
# views.py
from django.contrib.auth import authenticate, login
from django.core.cache import cache
from django.http import HttpResponseForbidden

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        
        # Rate limiting (5 attempts per 15 minutes)
        cache_key = f'login_attempts_{username}'
        attempts = cache.get(cache_key, 0)
        
        if attempts >= 5:
            return HttpResponseForbidden("Too many login attempts")
        
        user = authenticate(request, username=username, password=request.POST.get('password'))
        
        if user is None:
            cache.set(cache_key, attempts + 1, timeout=900)  # 15 min
            return render(request, 'login.html', {'error': 'Invalid credentials'})
        
        cache.delete(cache_key)
        login(request, user)
        # ...
```

#### A09:2021 - Security Logging and Monitoring Failures

**For educational apps:**
- Track unusual progress patterns (cheating detection)
- Monitor audio file access (prevent mass downloading)
- Log authentication failures

```python
# middleware.py
import logging

logger = logging.getLogger('security')

class SecurityLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Log sensitive actions
        if request.path.startswith('/api/progress'):
            logger.info(f"Progress update: {request.user.username} - {request.method}")
        
        response = self.get_response(request)
        return response
```

### 3.2 PWA-Specific Security Risks

From cside.com research on PWA dangers:
> "PWAs are browsers at their core. Every app becomes a micro-web environment. Building a PWA amplifies client-side security risks by bringing them into your app."

**Specific to Coreano Marcial:**

1. **Service Worker Hijacking**
   - If attacker gains access to service-worker.js source, they can intercept all network requests
   - Mitigation: Subresource Integrity (SRI) checks, HTTPS-only, frequent audits

2. **Cached Audio Tampering**
   - Malicious actor replaces cached audio files with incorrect pronunciation
   - Mitigation: Cache integrity checks, audio file hashing

3. **Manifest Poisoning**
   - Cross-site scripting allows attacker to link their own manifest
   - Mitigation: Strict CSP, validate manifest source

**Implementation:**
```javascript
// service-worker.js - Integrity checking
const AUDIO_HASHES = {
    'annyeonghaseyo.mp3': 'sha256-abc123...',
    // ... hash for each audio file
};

self.addEventListener('fetch', (event) => {
    if (event.request.url.includes('/audio/')) {
        event.respondWith(
            caches.match(event.request).then(response => {
                if (response) {
                    // Verify cache integrity
                    return response.blob().then(blob => {
                        return crypto.subtle.digest('SHA-256', blob)
                            .then(hash => {
                                // Compare hash, return response or re-fetch
                            });
                    });
                }
                return fetch(event.request);
            })
        );
    }
});
```

---

## 4. Critical Implementation Challenges

### 4.1 Content Creation & Maintenance

**Reality Check:**

For a comprehensive martial arts Korean curriculum:
- Minimum 500 vocabulary terms (White to Black Belt)
- Each term needs:
  - Native speaker audio (male + female for dialect awareness)
  - Written Hangul
  - Pronunciation breakdown (phoneme level)
  - Context sentences
  - Visual aids (for physical techniques)

**Workload:**
- 500 terms × 2 audio files × 30 seconds = ~8 hours of audio
- Recording time: 3-4x actual audio length = 24-32 hours
- Post-production (editing, normalization): 2x recording time = 48-64 hours
- **Total:** 80-100+ hours for audio alone

**Maintenance:**
- Audio re-recording when errors found
- Terminology updates (KKW/WTF standard changes)
- Dialect variations (Seoul vs Busan Korean)

### 4.2 Pedagogical Design Challenges

**Zero Romanization Mandate:**

Pro: Linguistically correct, prevents bad habits  
Con: Steep learning curve for complete beginners

**Risk:** Users unfamiliar with Hangul will be blocked from Day 1 unless:
- Pre-course Hangul learning module included
- Progressive romanization removal (controversial)
- Extensive audio support compensates

**Belt Progression System:**

Traditional martial arts: 10 kup → 1 kup → 1 dan  
Language learning: Non-linear, individualized pace

**Mismatch:** Forcing martial arts hierarchy onto language learning may:
- Demotivate faster learners (artificial gate-keeping)
- Frustrate slower learners (pressure to advance)
- Ignore that vocabulary and pronunciation develop at different rates

**Alternative:** Competency-based progression decoupled from belt metaphor?

### 4.3 Mobile-First Constraints

**Testing Burden:**

Must test on:
- iOS (Safari, Chrome, Firefox)
- Android (Chrome, Samsung Internet, Firefox)
- Various screen sizes (320px - 428px width)
- Offline/online transitions
- Low-bandwidth scenarios
- Storage quota exhaustion

**Django doesn't help here** - responsive design is entirely on your CSS/HTML.

**Audio Playback Issues:**

iOS Safari:
- Requires user interaction to play audio (no autoplay)
- Background audio requires specific manifest configuration
- Bluetooth headset compatibility issues

Android:
- Varies by browser and OEM
- Background audio more permissive but inconsistent

### 4.4 Accessibility Requirements

**WCAG 2.1 Compliance for Educational Apps:**

- Audio must have text transcripts (Korean + Translation)
- Visual progress indicators need ARIA labels
- Keyboard navigation for all interactions (HTMX default is click-focused)
- Screen reader compatibility (test with VoiceOver, TalkBack)

**HTMX Accessibility:**
```html
<!-- Good: Accessible HTMX button -->
<button 
    hx-get="/next-lesson"
    hx-target="#lesson-content"
    hx-indicator="#loading"
    aria-label="Load next lesson"
    aria-busy="false"
    aria-live="polite">
    Next
</button>

<div id="loading" role="status" aria-live="polite" aria-atomic="true" class="htmx-indicator">
    Loading...
</div>
```

---

## 5. Recommended Tech Stack Refinements

### 5.1 Core Stack Validation

✅ **Django:** Solid choice  
- Mature, secure, well-documented  
- ORM prevents SQL injection  
- Built-in admin for content management  
- Django REST Framework available if you need API later

✅ **HTMX:** Good for this use case  
- Server-driven architecture aligns with "backend as truth"  
- Reduces JavaScript complexity  
- BUT: Requires disciplined template organization

⚠️ **PWA:** Proceed with caution  
- Offline audio is useful for learners  
- BUT: Browser support inconsistencies, especially Safari  
- Service worker security requires expertise  
- Consider: "Enhanced Website" instead of full PWA initially

### 5.2 Recommended Additions

**1. Alpine.js (~15KB)**
```html
<!-- For simple client-side interactivity HTMX can't handle -->
<div x-data="{ playing: false }">
    <button 
        @click="playing = !playing; $refs.audio.play()"
        x-text="playing ? 'Pause' : 'Play'">
    </button>
    <audio x-ref="audio" src="/audio/example.mp3"></audio>
</div>
```

**2. django-htmx Package**
```python
# Simplifies HTMX detection
def lesson_view(request):
    if request.htmx:  # Cleaner than header checking
        return render(request, 'fragments/lesson.html')
    return render(request, 'pages/lesson.html')
```

**3. Tailwind CSS (via CDN for MVP)**
- Avoids webpack/build step complexity
- Mobile-first by default
- BUT: Consider long-term build pipeline

**4. django-storages + S3/Cloudflare R2**
- Don't serve audio from Django (inefficient)
- CDN reduces latency
- Signed URLs prevent hotlinking

### 5.3 What NOT to Do

❌ **Don't:** Build pronunciation assessment yourself  
- Requires ML expertise  
- Training data collection  
- You'll spend 6 months on 1 feature  
✅ **Do:** Use Speechace or Azure API, accept limitations

❌ **Don't:** Over-engineer offline sync  
- Start with simple "view offline, sync on reconnect"  
- Background Sync API not worth the complexity initially

❌ **Don't:** Build custom audio player  
- HTML5 `<audio>` element is sufficient  
- Libraries like Howler.js are overkill for this use case

❌ **Don't:** Create SPA-like single-page experience from Day 1  
- HTMX enables it, but adds complexity  
- Start with traditional multi-page app, enhance progressively

---

## 6. Development Phases & Risk Mitigation

### Phase 0: Foundation (4-6 weeks)
**Goal:** Validate core concept with minimal technical debt

**Deliverables:**
- Django project structure
- User authentication (Django built-in)
- Basic lesson model (Korean term, translation, audio URL)
- 10 sample lessons
- HTML5 audio playback (no HTMX yet)
- Mobile-responsive CSS (Tailwind CDN)

**Risks Addressed:**
- Proves content creation is feasible
- Tests audio quality/file size
- Validates user interest before PWA investment

### Phase 1: Interactive Learning (6-8 weeks)
**Goal:** Add HTMX interactivity, belt progression

**Deliverables:**
- HTMX integration
- Lesson navigation without page reloads
- User progress tracking
- Belt advancement logic
- 50+ lessons across 2 belt levels

**Risks:**
- Template proliferation (mitigate with _fragments/ organization)
- CSRF token handling (test thoroughly)

### Phase 2: PWA Conversion (4-6 weeks)
**Goal:** Offline capability

**Deliverables:**
- Service worker (basic caching)
- Manifest.json
- Offline lesson viewing
- Audio pre-caching (user-initiated)

**Risks:**
- Safari storage limits (set expectations)
- Service worker bugs (test exhaustively)

### Phase 3: Pronunciation (8-12 weeks)
**Goal:** AI-assisted pronunciation feedback

**Deliverables:**
- Third-party API integration (Azure or Speechace)
- Recording UI
- Feedback display
- Error handling (noise, API failures)

**Risks:**
- API costs (monitor usage)
- User frustration with false negatives (UX messaging critical)

### Phase 4: Refinement (Ongoing)
- Content expansion
- Community features (optional)
- Analytics
- Performance optimization

---

## 7. Cost & Resource Reality Check

### 7.1 Development Time

**Solo Developer (experienced with Django):**
- Phase 0-2: 4-6 months part-time (20 hrs/week)
- Phase 3: +2-3 months
- **Total to "feature complete" MVP:** 6-9 months

**Team (2 developers):**
- Phase 0-2: 3-4 months
- Phase 3: +1-2 months
- **Total:** 4-6 months

### 7.2 Ongoing Costs

**Infrastructure:**
- Hosting (Django + Postgres): $20-50/month (Digital Ocean, Heroku, Railway)
- Audio CDN (Cloudflare R2): $0-15/month (depends on usage)
- Pronunciation API: $0.001-0.004 per assessment (budget $50-200/month for 5000-10000 assessments)

**Content Creation:**
- Native speaker recordings: $500-2000 (freelance voice actors)
- Audio editing: 20-40 hours @ $25-50/hr = $500-2000
- **OR:** DIY if you have access to native speakers (free but time-intensive)

**Maintenance:**
- Security updates: 2-4 hrs/month
- Content fixes: 4-8 hrs/month
- User support: Variable

### 7.3 Hidden Costs

- **Browser compatibility testing:** 20-40 hours over project lifetime
- **Accessibility audit:** $500-2000 if outsourced
- **Legal:** Terms of Service, Privacy Policy drafting ($300-1000)
- **Audio licensing:** If using copyrighted recordings (variable)

---

## 8. Critical Risks & Break Points

### 8.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Service worker bugs block entire app | Medium | Critical | Extensive testing, feature flags, fallback to regular website |
| iOS Safari storage limits frustrate users | High | Medium | Clear UX about storage, prioritize most-used content |
| Pronunciation API inaccuracy demotivates learners | High | High | Transparent messaging, manual review option, thresholds |
| HTMX template organization becomes unmaintainable | Medium | High | Strict conventions from Day 1, documentation |
| Audio file size exceeds PWA quotas | Medium | Medium | Compression (Opus codec), user-initiated downloads |

### 8.2 Conceptual Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Market too niche (martial artists who want to learn Korean) | High | Critical | Validate demand before full build, expand to general Korean if needed |
| Zero romanization creates learning barrier | Medium | High | Hangul primer module, extensive audio support |
| Belt progression doesn't align with learning pace | Medium | Medium | Flexible advancement criteria, optional linear mode |
| Users expect gamification (points, streaks) not provided | Medium | Low | Add later if user feedback demands it |

### 8.3 Maintenance Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Audio content becomes outdated | Low | Medium | Version control for audio, update roadmap |
| Martial arts terminology standards change | Low | Low | Modular content structure allows updates |
| Solo developer burnout | High | Critical | Phase project, set realistic timelines, consider this a long-term commitment |

---

## 9. Security Checklist (Pre-Launch)

### Required Before Production:

- [ ] HTTPS enforced (Let's Encrypt certificate)
- [ ] DEBUG = False in settings.py
- [ ] SECRET_KEY in environment variable, not code
- [ ] ALLOWED_HOSTS restricted to production domain
- [ ] CSRF protection enabled (Django default, but verify HTMX integration)
- [ ] CSP headers configured
- [ ] Session cookies: Secure, HttpOnly, SameSite=Strict
- [ ] Rate limiting on login, API endpoints
- [ ] User input sanitized (Django default, but verify custom code)
- [ ] SQL injection protection (Django ORM, but audit raw queries)
- [ ] File upload validation (if allowing user content)
- [ ] Service worker integrity checks
- [ ] Dependency audit (pip-audit or Safety)
- [ ] Security headers (django-csp, django-secure)
- [ ] Logging configured (errors, security events)
- [ ] Backup strategy for database
- [ ] Privacy policy (GDPR considerations if EU users)
- [ ] Terms of service

### Ongoing Security:

- [ ] Monthly dependency updates
- [ ] Quarterly security audit
- [ ] Monitor Django security mailing list
- [ ] Log review (weekly)

---

## 10. Honest Conclusion: Should This Project Exist?

### ✅ Reasons to Build It:

1. **Genuine Gap:** No comprehensive martial arts-focused Korean learning platform exists
2. **Technical Feasibility:** Django + HTMX is proven, well-documented
3. **Educational Value:** Zero romanization + audio-first is pedagogically sound
4. **Personal Growth:** If building for learning, this is a complex-enough project without being overwhelming

### ⚠️ Reasons to Reconsider:

1. **Niche Market:** Martial artists who want to learn Korean is a small TAM (Total Addressable Market)
   - Consider: Expand scope to "Korean for Physical Activities" (sports, dance, fitness)?
2. **Maintenance Burden:** Audio content requires ongoing updates, native speakers, quality control
3. **Pronunciation Assessment:** Third-party APIs are imperfect, costs add up, offline mode limited
4. **PWA Complexity:** Safari limitations, service worker security risks, storage quotas
5. **Time Investment:** 6-9 months to MVP for solo developer is significant

### Verdict: **Proceed with Caution**

**This project is technically viable but requires:**
- Realistic timeline (9+ months to launch)
- Budget for pronunciation API ($50-200/month ongoing)
- Access to native Korean speakers for content creation
- Strong discipline in code organization (HTMX template sprawl)
- Acceptance that niche market may limit adoption

**Recommended Path:**

1. **Validate demand FIRST**
   - Build landing page with email signup
   - Survey martial arts communities (Reddit, Facebook groups)
   - Get 100+ interested users before building

2. **Start Small**
   - Phase 0 only (basic Django app, no PWA)
   - 20 lessons, simple progression
   - Test with beta users

3. **Iterate Based on Feedback**
   - Does zero romanization work? Users might demand it
   - Is pronunciation assessment worth the cost? Maybe listening practice is enough
   - Do users care about offline mode? Desktop users won't

4. **Expand Cautiously**
   - Add PWA only if offline use is validated as critical
   - Add pronunciation API only if budget allows and users request it
   - Consider general Korean market if martial arts niche too small

**Final Thought:**

This project is feasible but **not easy**. The combination of Django + HTMX + PWA + audio content + security requirements creates a deceptively complex system. The stack is solid, but the domain (language learning) has high expectations (Duolingo exists) and the niche (martial arts) limits scale.

If you're building this:
- For learning: Excellent project, will teach you advanced Django, HTMX, PWA, audio handling
- For profit: Validate market demand first, have a monetization plan
- For community: Make it open source, accept it's a labor of love

**You should NOT start building unless:**
- You have 6-9 months to commit
- You have budget for API costs ($500-1000/year minimum)
- You have access to native Korean speakers
- You're comfortable with the security responsibility of user data
- You have a plan for what happens if you can't maintain it long-term

---

## 11. Reference Materials

### Official Documentation:
- Django: https://docs.djangoproject.com/
- HTMX: https://htmx.org/
- MDN PWA: https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps
- OWASP Top 10: https://owasp.org/www-project-top-ten/

### Recommended Reading:
- Django+HTMX tutorial: https://harabat.github.io/django-htmx/
- PWA Security Best Practices: https://blog.pixelfreestudio.com/best-practices-for-pwa-security/
- HTMX Web Security: https://htmx.org/essays/web-security-basics-with-htmx/

### Code Repositories (study these):
- django-htmx: https://github.com/adamchainz/django-htmx
- django-htmx-spa example: https://github.com/PetrJoe/django-htmx-spa

### Pronunciation APIs:
- Azure Pronunciation Assessment: https://learn.microsoft.com/en-us/legal/cognitive-services/speech-service/pronunciation-assessment/
- Speechace: https://www.speechace.com/api-plans/
- SpeechSuper: https://www.speechsuper.com/

---

**Document Maintainer:** Claude  
**Review Cycle:** Update before each development phase  
**Status:** ⚠️ Critical Review - Proceed Only After Validation
