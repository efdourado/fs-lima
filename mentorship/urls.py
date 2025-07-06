from django.urls import path
from . import views

urlpatterns = [
    path('', views.mentorship, name='mentorship'),
    path('meetings/', views.meetings, name='meetings'),
    path('auth/', views.auth, name="auth_mentee"),
    path('choose_day/', views.choose_day, name='choose_day'),
    path('book_meeting/', views.book_meeting, name='book_meeting'),
]