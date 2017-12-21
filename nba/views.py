from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests

# Create your views here.
def get_all_nba_teams():
	nba_teams = []
	r = requests.get("http://data.nba.net/data/1h/prod/2017/teams_config.json")
	r = r.json()['teams']['config']
	for i in r:
		if i['web']['homepage'] != "":
			nba_teams.append(i['ttsName'])
	return nba_teams

# start page
def nba_teams(request):		
	nba_teams = get_all_nba_teams()
	template = loader.get_template('nba/nba_teams.html')
	context = {
		'nba_teams': nba_teams,
	}
	return HttpResponse(template.render(context, request))
