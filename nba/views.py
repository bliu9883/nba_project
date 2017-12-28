from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Team, Player
import requests

# Create your views here.
def get_all_nba_teams():
	r = requests.get("http://data.nba.net/data/10s/prod/v1/2017/teams.json")
	r = r.json()['league']['standard']
	for i in r:
		if i['isNBAFranchise']:
			# nba_teams.append({'teamId': i['teamId'], 'fullName': i['fullName'], 'tricode': i['tricode']})		
			team = Team(id=i['teamId'], team_name=i['fullName'], tri_code=i['tricode'])
			team.save()

def get_team_colors():
	r = requests.get("http://data.nba.net/data/1h/prod/2017/teams_config.json")
	r=r.json()['teams']['config']
	for i in r:
		if Team.objects.filter(id=i['teamId']).exists():
			team = Team.objects.get(id=i['teamId'])
			team.color = i['primaryColor']
			team.save()
	
# start page
def nba_teams(request):		
	get_all_nba_teams()
	teams = Team.objects.order_by('team_name')
	get_team_colors()
	template = loader.get_template('nba/nba_teams.html')
	context = {
		'teams': teams,
	}
	return HttpResponse(template.render(context, request))

def get_players_on_team(teamId):
	r = requests.get("http://data.nba.net/data/10s/prod/v1/2017/players.json")
	r = r.json()['league']['standard']
	for i in r:
		if str(teamId) == i['teamId']:
			player = Player(id=i['personId'], 
							team=Team.objects.get(id=teamId),
							first_name=i['firstName'],
							last_name=i['lastName'])
			player.save()
	
# get team info using tricode as link
def team_info(request, tri_code):
	team = Team.objects.get(tri_code=tri_code)
	get_players_on_team(team.id)
	players = team.player_set.all().order_by('last_name')
	template = loader.get_template('nba/team_roster.html')
	context = {
		'players': players,
	}
	return HttpResponse(template.render(context, request))
