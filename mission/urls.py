"""
URL routes for the Sol Survivor Mission Control app.
"""

from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('mission/', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard_alias'),
    path('logout/', views.logout_view, name='logout'),
    path('manifest.json', TemplateView.as_view(template_name='mission/manifest.json', content_type='application/json'), name='mission_manifest'),
    path('sw.js', TemplateView.as_view(template_name='mission/sw.js', content_type='application/javascript'), name='mission_sw'),
    path('api/action/', views.api_action, name='api_action'),
    path('api/cli/', views.api_cli_command, name='api_cli'),
    path('api/ai_chat/', views.api_ai_chat, name='api_ai_chat'),
    path('api/forecast/', views.api_forecast, name='api_forecast'),
    path('api/nasa_data/', views.api_nasa_data, name='api_nasa_data'),
    path('api/submit_quiz/', views.api_submit_quiz, name='api_submit_quiz'),
    path('report/', views.mission_report_view, name='mission_report'),
    path('certificate/', views.certificate_view, name='certificate'),
    # Space Academy & Educational Mini-Games Routes
    path('academy/', views.academy_view, name='academy'),
    path('academy/<str:game_id>/', views.academy_game_view, name='academy_game'),
    path('api/academy/set_profile/', views.api_academy_set_profile, name='api_academy_set_profile'),
    path('api/academy/submit_score/', views.api_academy_submit_score, name='api_academy_submit_score'),
    path('api/academy/progress/', views.api_academy_progress, name='api_academy_progress'),
]
