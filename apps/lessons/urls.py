"""
URLs for lesson views.
"""
from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('belt/<int:belt_id>/', views.BeltDetailView.as_view(), name='belt_detail'),
    path('lesson/<int:lesson_id>/', views.LessonDetailView.as_view(), name='lesson_detail'),
]
