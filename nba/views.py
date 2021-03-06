from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Team, Player, Schedule
import requests, datetime, pytz
from django.utils import timezone

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
								division=i['divName'],
								url="http://stats.nba.com/media/img/teams/logos/" + i['tricode'] + "_logo.svg",
								)
					team.cache()
					team.save()
				else:
					break;
			else:
				team = Team(id=i['teamId'], 
							team_name=i['fullName'], 
							tri_code=i['tricode'],
							conference=i['confName'],
							division=i['divName'],
							url="http://stats.nba.com/media/img/teams/logos/" + i['tricode'] + "_logo.svg",
							)
				team.cache()
				team.save()

def get_team_colors():
	r = requests.get("http://data.nba.net/data/1h/prod/2017/teams_config.json")
	r=r.json()['teams']['config']
	for i in r:
		if Team.objects.filter(id=i['teamId']).exists():
			team = Team.objects.get(id=i['teamId'])
			if team.color == "":
				team.color = i['primaryColor']
				team.save()

def get_current_standings():
	now = datetime.datetime.now()
	r = ""
	try:
		date = str(now.year) + '%02d'%now.month + '%02d'%now.day
		r = requests.get("http://data.nba.net/data/10s/prod/v1/" + date +"/standings_all.json")
		r = r.json()['league']['standard']['teams']
	except:
		date = str(now.year) + '%02d'%now.month + '%02d'%(now.day-1)
		r = requests.get("http://data.nba.net/data/10s/prod/v1/" + date +"/standings_all.json")
		r = r.json()['league']['standard']['teams']
	for i in r:
		team = Team.objects.get(id=i['teamId'])
		team.wins = i['win']
		team.losses = i['loss']
		team.save()

# start page
def nba_teams(request):		
	get_all_nba_teams()
	teams = Team.objects.order_by('team_name')
	get_team_colors()
	get_current_standings()
	template = loader.get_template('nba/nba_teams.html')
	context = {
		'teams': teams,
	}
	return HttpResponse(template.render(context, request))

def get_player_stats(player):
	r = requests.get("http://data.nba.net/data/10s/prod/v1/2017/players/" + str(player.id) + "_profile.json")
	r = r.json()['league']['standard']['stats']['latest']
	player.points = r['ppg'] if r['ppg'] != '-1' else 'N/A'
	player.rebounds = r['rpg'] if r['rpg'] != '-1' else 'N/A'
	player.assists = r['apg'] if r['apg'] != '-1' else 'N/A'
	
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
									last_name=i['lastName'],
									jersey=i['jersey'],
									height=i['heightFeet']+ "\'" + i['heightInches'] + '\"',
									weight=i['weightPounds'],
									dob=i['dateOfBirthUTC'],
									position=i['pos'],
									college=i['collegeName'],
									draft=i['draft']['seasonYear'] + " Round: " +i['draft']['roundNum'] + " Pick: " + i['draft']['pickNum'],
									url="https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/"+ i['personId'] +".png"
									)
					get_player_stats(player)
					player.cache()
					player.save()
				else:
					break;
			else:
				player = Player(id=i['personId'], 
								team=Team.objects.get(id=teamId),
								first_name=i['firstName'],
								last_name=i['lastName'],
								jersey=i['jersey'],
								height=i['heightFeet']+ "\'" + i['heightInches'] + '\"',
								weight=i['weightPounds'] + "lbs",
								dob=i['dateOfBirthUTC'],
								position=i['pos'],
								college=i['collegeName'],
								draft=i['draft']['seasonYear'] + " Round: " +i['draft']['roundNum'] + " Pick: " + i['draft']['pickNum'],
								url="https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/"+ i['personId'] +".png",)
				get_player_stats(player) 
				player.cache()
				player.save()

	
				
def get_team_schedule(teamId):
	r = requests.get("http://data.nba.net/data/10s/prod/v1/2017/teams/" + str(teamId) + "/schedule.json")
	r = r.json()['league']['standard']
	for i in r:
		dateUTC = i['startTimeUTC']
		gameTime = datetime.datetime(int(dateUTC[:4]), int(dateUTC[5:7]), int(dateUTC[8:10]), int(dateUTC[11:13]), int(dateUTC[14:16]), int(dateUTC[17:19]), int(dateUTC[20:22]), pytz.UTC)
		if Schedule.objects.filter(gameId=Team.objects.get(id=teamId).tri_code + "" + i['gameId']).exists():
			s = Schedule.objects.get(gameId=Team.objects.get(id=teamId).tri_code + "" + i['gameId'])
			if s.score and s.opponentScore:
				continue
			if i['statusNum']==3 and not s.score and not s.opponentScore:
				s.score = int(i['hTeam']['score']) if s.isHomeTeam else int(i['vTeam']['score'])
				s.opponentScore = int(i['vTeam']['score']) if s.isHomeTeam else int(i['vTeam']['score'])
				s.save()
		else:
			if i['seasonStageId']==2:
				isHomeTeam = i['isHomeTeam']
				opponentTeamId = int(i['hTeam']['teamId']) if not isHomeTeam else int(i['vTeam']['teamId'])
				score = None
				opponentScore=None
				if i['statusNum']==3:
					score = int(i['hTeam']['score']) if isHomeTeam else int(i['vTeam']['score'])
					opponentScore = int(i['hTeam']['score']) if not isHomeTeam else int(i['vTeam']['score'])
					game = Schedule(gameId=Team.objects.get(id=teamId).tri_code + "" + i['gameId'],
									date=gameTime,
									team=Team.objects.get(id=teamId),
									opponent=Team.objects.get(id=opponentTeamId),
									isHomeTeam=isHomeTeam,
									score=score,
									opponentScore=opponentScore)
					game.save()
				else:
					game = Schedule(gameId=Team.objects.get(id=teamId).tri_code + "" + i['gameId'],
									date=gameTime,
									team=Team.objects.get(id=teamId),
									opponent=Team.objects.get(id=opponentTeamId),
									isHomeTeam=isHomeTeam)
					game.save()
		

# get team info using tricode as link
def team_info(request, tri_code):
	team = Team.objects.get(tri_code=tri_code)
	get_players_on_team(team.id)
	get_team_schedule(team.id)
	players = team.player_set.all().order_by('last_name')
	schedule = team.team.filter(date__lt=timezone.now()).order_by('-date')[:5][::-1]
	template = loader.get_template('nba/team_roster.html')
	context = {
		'team': team,
		'players': players,
		'schedule': schedule,
	}
	return HttpResponse(template.render(context, request))

def player_info(request, tri_code, playerId):
	player = Player.objects.get(id=playerId)
	template = loader.get_template('nba/player_info.html')
	context = {
		'player': player,
	}
	return HttpResponse(template.render(context, request))
