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
			if Team.objects.filter(id=i['teamId']).exists():
				if not Team.objects.get(id=i['teamId']).was_updated_recently():
					team = Team(id=i['teamId'], 
								team_name=i['fullName'], 
								tri_code=i['tricode'],
								conference=i['confName'],
								division=i['divName'])
					team.save()
				else:
					break;
			else:
				team = Team(id=i['teamId'], 
							team_name=i['fullName'], 
							tri_code=i['tricode'],
							conference=i['confName'],
							division=i['divName'])
				team.save()

def get_team_colors():
	r = requests.get("http://data.nba.net/data/1h/prod/2017/teams_config.json")
	r=r.json()['teams']['config']
	for i in r:
		if Team.objects.filter(id=i['teamId']).exists():
			team = Team.objects.get(id=i['teamId'])
			if team.color == None:
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
	team = Team.objects.get(id=teamId)
	for i in r:
		if str(teamId) == i['teamId']:
			if Player.objects.filter(id=i['personId']).exists():
				if not Player.objects.get(id=i['personId']).was_updated_recently():
					player = Player(id=i['personId'], 
									team=team,
									first_name=i['firstName'],
									last_name=i['lastName'])
					player.save()
				else:
					break;
			else:
				player = Player(id=i['personId'], 
								team=Team.objects.get(id=teamId),
								first_name=i['firstName'],
								last_name=i['lastName'])
				player.save()
				
def get_player_current_stats(teamId):
	team = Team.objects.get(id=teamId)
	players = team.player_set.all()
	for i in players:
		if Player.objects.filter(id=i.id).exists():
			player = Player.objects.get(id=i.id)
			r = requests.get("http://data.nba.net/data/10s/prod/v1/2017/players/" + str(i.id) + "_profile.json")
			r = r.json()['league']['standard']['stats']['latest']
			player.points = r['ppg']
			player.rebounds= r['rpg']
			player.assists = r['apg']
			player.save()

# get team info using tricode as link
def team_info(request, tri_code):
	team = Team.objects.get(tri_code=tri_code)
	get_players_on_team(team.id)
	get_player_current_stats(team.id)
	players = team.player_set.all().order_by('last_name')
	template = loader.get_template('nba/team_roster.html')
	context = {
		'team': team,
		'players': players,
	}
	return HttpResponse(template.render(context, request))

def player_info(request, tri_code, playerId):
	player = Player.objects.get(id=playerId)
	template = loader.get_template('nba/player_info.html')
	context = {
		'player': player,
	}
	return HttpResponse(template.render(context, request))
