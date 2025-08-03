from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('projects/new/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/hire/', views.hire_now, name='hire_now'),
path('projects/<int:pk>/', views.project_view, name='project_view'),
path('users/search/', views.search_users, name='search_users'),
path('notifications/', views.notifications_view, name='notifications'),
path('messages/', views.messages_view, name='messages'),
path('hire/<int:user_id>/', views.hire_now, name='hire_now'),
    path('message/<int:user_id>/', views.send_message, name='send_message'),
path('projects/<int:project_id>/like/', views.like_project, name='like_project'),
    path('projects/<int:project_id>/delete/', views.delete_project, name='delete_project'),

    path('profile/', views.user_profile, name='user_profile'),
    path('messages/send/', views.compose_message, name='compose_message'),


]
