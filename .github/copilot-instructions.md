# Copilot / Agent Quick Instructions ✅

Purpose: Help AI coding agents be immediately productive in this Django monolith (Coreano Marcial).
Keep changes small and well-tested — most content is edited via Django Admin.

## Project at-a-glance 🔍
- Framework: **Django 4.2** (monolithic backend + server-rendered templates).
- Domain apps: `apps/lessons`, `apps/progress`, `apps/audio`, `apps/users` (each implements models, views, urls, admin).
- Data & files: PostgreSQL (env-configured) + uploaded audio under `media/`.
- Content management: **Django Admin** is the primary authoring surface for lessons, belts, vocabulary and audio.

## Quick dev setup (exact commands) ▶️
1. Create venv and install deps:
   ```bash
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copy env and set secrets (required):
   ```bash
   cp .env.example .env
   # Edit .env - DJANGO_SECRET_KEY is required (settings raises if missing)
   ```
3. DB & migrations:
   ```bash
   createdb coreano_marcial
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Prepare logs and admin:
   ```bash
   mkdir -p logs
   python manage.py createsuperuser
   python manage.py runserver
   ```

## Important repo-specific notes 🧭
- `config/settings.py` reads critical env vars and will raise if `DJANGO_SECRET_KEY` is missing. **Do not commit secrets.**
- `AUTH_USER_MODEL` is `users.CustomUser` — altering the user model requires careful migration planning.
- Static vs media: `STATICFILES_DIRS` -> `static/`; uploaded audio and media go to `media/`. Media is served by `django` only if `DEBUG` is True (`config/urls.py`).
- Logging writes to `logs/django.log` and `logs/security.log` — ensure `logs/` exists in dev.

## Patterns & conventions to follow 🧩
- Domain separation: add new features inside the appropriate app under `apps/` (models, views, urls, admin). Keep domain logic in `models.py` or `services` modules.
- Views that return user-specific content use `LoginRequiredMixin` (see `apps/lessons/views.py`). Follow the same pattern for new views.
- Database constraints are used explicitly (e.g., `unique_together` on lessons, `ordering` in BeltLevel). Mimic existing DB constraints when adding fields.
- Audio handling: `apps/audio/models.py` enforces file extensions via `validate_audio_extension` (allowed: `.mp3`, `.ogg`, `.opus`) and `clean()` ensures audio is tied to either a Lesson or a VocabularyItem, not both.
- Progress rules live in `apps/progress/models.py` (see `UserProgress.can_advance_to_next_belt` and the `post_save` signal creating `UserProgress`). If you change progression logic, update tests and admin fixtures.

## Tests & CI ⚙️
- There are no tests or GitHub Actions workflows yet. Tests should live under `tests/` following the `.specify` templates.
- Use Django's test runner (`python manage.py test`) for small changes; the repo references `pytest`/`ruff` in `.specify` templates — if introduced, document the commands clearly in README and CI.

## Where to look first when debugging 🐞
- Settings/env issues: `config/settings.py` (missing env vars will raise on import).
- URL routing: `config/urls.py` (media/static only served in DEBUG).
- Data logic and constraints: `apps/lessons/models.py`, `apps/progress/models.py`, `apps/audio/models.py`.

## Safety & code practice ⚠️
- **Never** commit `.env` or real secret keys.
- Local dev: set `DEBUG=True` in `.env` (production should be `False`). Cookie/security flags are set in `settings.py` (session & CSRF cookies are secure by default).

## Examples (copy-paste) ✂️
- Run migrations & start server:
  ```bash
  python manage.py migrate && python manage.py runserver
  ```
- Run shell to inspect models:
  ```bash
  python manage.py shell
  from apps.lessons.models import BeltLevel
  BeltLevel.objects.all()
  ```

---
If anything here is unclear or you want more detail on testing, CI, or the belt-progression rules, tell me which section to expand and I’ll iterate. ✅
