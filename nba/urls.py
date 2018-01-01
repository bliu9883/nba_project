from django.urls import path

from . import views

app_name = 'nba'
urlpatterns = [
	path('', views.nba_teams, name='nba_teams'),
	path('team/<str:tri_code>/', views.team_info, name='team_info'),
	path('<str:tri_code>/player/<int:playerId>', views.player_info, name='player_info'),
]