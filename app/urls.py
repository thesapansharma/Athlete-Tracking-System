# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [
    re_path(r'^.*\.html', views.pages, name='pages'),

    path('', views.index, name='home'),
    path('weekly-reflection/', views.weekly_reflection, name='weekly_reflection'),
     path('events/manage/', views.manage_events, name='manage_events'),
    path('events/update/<int:event_id>/', views.update_event, name='update_event'),
     path('competitions/old/<int:event_id>/', views.competition_results, name='competition_results'),
    path('events/create/', views.manage_events, name='create_event'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('competitions/old/', views.old_competitions, name='old_competitions'),
    path('competitions/upcoming/', views.upcoming_competitions, name='upcoming_competitions'),
    path('results/<int:competition_id>/', views.results, name='results'),
    path('events/manage/', views.manage_events, name='manage_events'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
     path('results/', views.result_list, name='result_list'),
    path('results/create/', views.create_result, name='create_result'),
    path('athlete-progress/<int:athlete_id>/', views.athlete_progress_report, name='athlete_progress_report'),
    path('diet/', views.diet_dashboard, name='diet_dashboard'),
    path('diet/download/<int:diet_plan_id>/', views.download_diet_pdf, name='download_diet_pdf'),
    path('diet/add/', views.add_diet_plan, name='add_exercise_plan'),
    path('exercise/', views.exercise_dashboard, name='exercise_dashboard'),
    path('exercise/download/<int:exercise_plan_id>/', views.download_exercise_pdf, name='download_exercise_pdf'),
    path('exercise/add/', views.add_exercise_plan, name='add_exercise_plan'),
    path('task/', views.task_checklist, name='task_checklist'),
    path('update-task-status/<int:task_id>/', views.update_task_status, name='update_task_status'),
    path('conversation/<int:conversation_id>/', views.conversation_view, name='conversation_view'),
    path('create-conversation/<int:user_id>/', views.create_conversation, name='create_conversation'),
    path('start-conversation-with-coach/', views.start_conversation_with_coach, name='start_conversation_with_coach'),
    path('start-conversation-with-admin/', views.start_conversation_with_admin, name='start_conversation_with_admin'),
    path('admin-chat/conversations/', views.admin_conversations, name='admin_conversations'),
    path('coach/conversations/', views.coach_conversations, name='coach_conversations'),
    path('create_conversation/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('reflections/<int:athlete_id>/', views.list_reflections, name='list_reflections'),
    path('reflection/', views.reflections, name='reflections'),
    path('download_reflection/<int:reflection_id>/', views.download_reflection_pdf, name='download_reflection_pdf'),
    path('athletes/', views.user_list, name='user_list'),
    path('coach/', views.coach_list, name='user_list'),
    path('daily-reminders/', views.test_reminders, name='test_reminders'),
    path('weekly-reminders/', views.send_weekly_reflection_reminders, name='test_reminders'),
]
