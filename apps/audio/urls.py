"""
URLs for audio serving.
"""
from django.urls import path
from . import views

app_name = 'audio'

urlpatterns = [
    path('serve/<int:audio_id>/', views.serve_audio, name='serve_audio'),
]
