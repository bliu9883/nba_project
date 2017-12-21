from django.urls import path

from . import views

urlpatterns = [
	path('', views.nba_teams, name='nba_teams'),
]