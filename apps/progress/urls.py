"""
URLs for progress views.
"""
from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('advance-belt/', views.advance_belt, name='advance_belt'),
]
