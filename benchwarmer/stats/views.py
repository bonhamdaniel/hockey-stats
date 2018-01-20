from django.shortcuts import render
from django.http import HttpResponse
from django_tables2 import RequestConfig
from django.db.models import Q
from .tables import NhlTeamStats, summarizeTeamData, AhlSkaterSummary, ahlSkaterSummary, AhlSkaterSummaryRates, ahlSkaterSummaryRates, AhlSkaterSummaryPercentiles, ahlSkaterSummaryPercentiles, AhlOnIce, ahlOnIce, AhlScoringSituation, ahlScoringSituation
from .models import NhlTeam, NhlTeamSummary, NhlSeason, NhlGame, AhlSeason

def index(request):
	return render(request, 'stats/index.html')

def team(request):
	# set menus
	if 'seasonList' not in request.GET:
		choice = NhlSeason.objects.get(pk=19171918)
	else:
		choice = NhlSeason.objects.get(pk=request.GET['seasonList'])
	seasons = NhlSeason.objects.order_by('season_id')
	# prepare data
	if 'seasonList' not in request.GET:
		data = NhlTeamSummary.objects.filter(game_id__season_id=str(19171918))
	else:
		data = NhlTeamSummary.objects.filter(game_id__season_id=str(request.GET['seasonList']))
	data = data.filter(game_id__type='R')
	data = summarizeTeamData(data)
	table = NhlTeamStats(data, order_by='-gp')
	table.paginate(page=request.GET.get('page', 1), per_page=30)
	RequestConfig(request, paginate={'per_page': 30}).configure(table)
	context = {'choice': choice, 'seasons': seasons, 'table': table}
	return render(request, 'stats/team.html', context)

def players(request):
	# set menus
	# Season Menu
	if 'minSeason' not in request.GET or 'maxSeason' not in request.GET:
		season1Choice = AhlSeason.objects.get(pk=57)
		season2Choice = AhlSeason.objects.get(pk=57)
	else:
		season1Choice = AhlSeason.objects.get(pk=request.GET['minSeason'])
		season2Choice = AhlSeason.objects.get(pk=request.GET['maxSeason'])
	seasons = AhlSeason.objects.filter(Q(name__contains='Regular'))
	# Position Menu
	if 'position' not in request.GET:
		positionChoice = 1
	else:
		positionChoice = request.GET['position']
	# Max Games Played
	if 'minGames' not in request.GET:
		minGP = 0
	else:
		minGP = request.GET['minGames']
	# Age Span
	if 'minAge' not in request.GET:
		minAge = 18
	else:
		minAge = request.GET['minAge']
	if 'maxAge' not in request.GET:
		maxAge = 50
	else:
		maxAge = request.GET['maxAge']
	# Report Menu
	if 'report' not in request.GET:
		reportChoice = 1
	else:
		reportChoice = request.GET['report']
	if 'eraAdjust' in request.GET:
		adjust = 1
	else:
		adjust = 0
	# prepare data
	if int(reportChoice) == 1:
		data = ahlSkaterSummary(season1Choice, season2Choice, positionChoice, minGP, minAge, maxAge)
		table = AhlSkaterSummary(data, order_by='-p')
	elif int(reportChoice) == 2:
		data = ahlSkaterSummaryRates(season1Choice, season2Choice, positionChoice, minGP, minAge, maxAge)
		table = AhlSkaterSummaryRates(data, order_by='-p')
	elif int(reportChoice) == 3:
		data = ahlSkaterSummaryPercentiles(season1Choice, season2Choice, positionChoice, minGP, minAge, maxAge)
		table = AhlSkaterSummaryPercentiles(data, order_by='-p')
	elif int(reportChoice) <= 6:
		data = ahlOnIce(season1Choice, season2Choice, positionChoice, reportChoice, minGP, minAge, maxAge)
		table = AhlOnIce(data, order_by='-esfa')
	else:
		data = ahlScoringSituation(season1Choice, season2Choice, positionChoice, reportChoice, minGP, minAge, maxAge)
		table = AhlScoringSituation(data, order_by='-esp1')

	table.paginate(page=request.GET.get('page', 1), per_page=25)
	RequestConfig(request, paginate={'per_page': 25}).configure(table)
	context = {'season1Choice': season1Choice, 'season2Choice': season2Choice, 'positionChoice': positionChoice, 'reportChoice': reportChoice, 'minGP': minGP, 'minAge': minAge, 'maxAge': maxAge, 'seasons': seasons, 'table': table}
	return render(request, 'stats/players.html', context)

def teams(request):
	teams = NhlTeam.objects.order_by('-location')
	output = ', '.join([t.location for t in teams])
	return HttpResponse(output)