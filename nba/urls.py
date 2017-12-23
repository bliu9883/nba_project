from django.urls import path

from . import views

urlpatterns = [
	path('', views.nba_teams, name='nba_teams'),
	path('<str:tri_code>/', views.team_info, name='team_info'),
]