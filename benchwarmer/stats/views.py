from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django_tables2 import RequestConfig
from django.db.models import Q
from django.forms.models import model_to_dict
from django.db import connection
from .charts import BubbleChart
from .tables import NhlTeamStats, NhlSkaterSummary, nhlSkaterSummary, summarizeTeamData, AhlSkaterSummary, ahlSkaterSummary, AhlSkaterSummaryRates, ahlSkaterSummaryRates, AhlSkaterSummaryPercentiles, ahlSkaterSummaryPercentiles, AhlOnIce, ahlOnIce, AhlScoringSituation, ahlScoringSituation
from .models import NhlTeam, NhlTeamSummary, NhlSeason, NhlGame, AhlSeason, NhlPlayerBio, NhlPlayer

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
	# League Menu
	if 'league' not in request.GET:
		leagueChoice = 1
	else:
		leagueChoice = request.GET['league']
	# Get appropriateleague seasons
	if int(leagueChoice) == 1:
		leagueSeasons = NhlSeason.objects.all()
		seasons = NhlSeason.objects.all().order_by('-start_date')
	else:
		leagueSeasons = AhlSeason.objects.filter(Q(name__contains='Regular'))
		seasons = leagueSeasons
	# Season Menu
	if 'minSeason' not in request.GET or 'maxSeason' not in request.GET:
		season1Choice = leagueSeasons.order_by('-start_date')[0]
		season2Choice = leagueSeasons.order_by('-start_date')[0]
	else:
		season1Choice = leagueSeasons.get(pk=request.GET['minSeason'])
		season2Choice = leagueSeasons.get(pk=request.GET['maxSeason'])
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
		if int(leagueChoice) == 1:
			data = nhlSkaterSummary(season1Choice, season2Choice, positionChoice, minGP, minAge, maxAge)
			table = NhlSkaterSummary(data, order_by='-p')
		else:
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
	context = {'leagueChoice': leagueChoice, 'seasons': seasons, 'season1Choice': season1Choice, 'season2Choice': season2Choice, 'positionChoice': positionChoice, 'reportChoice': reportChoice, 'minGP': minGP, 'minAge': minAge, 'maxAge': maxAge, 'table': table}
	return render(request, 'stats/players.html', context)

def teams(request):
	teams = NhlTeam.objects.order_by('-location')
	output = ', '.join([t.location for t in teams])
	return HttpResponse(output)

def locations(request):
	# League Menu
	if 'league' not in request.GET:
		leagueChoice = '1'
	else:
		leagueChoice = request.GET['league']
	# MinSeason Menu
	if 'minSeason' not in request.GET:
		season1Choice = '20172018'
	else:
		season1Choice = request.GET['minSeason']
	# MaxSeason Menu
	if 'maxSeason' not in request.GET:
		season2Choice = '20172018'
	else:
		season2Choice = request.GET['maxSeason']
	# Position Menu
	if 'position' not in request.GET:
		positionChoice = '1'
	else:
		positionChoice = request.GET['position']
	# Skater Menu
	if 'skaters' not in request.GET:
		skaterChoice = '8479318'
	else:
		skaterChoice = request.GET['skaters']
	# Report Menu
	if 'report' not in request.GET:
		reportChoice = '4'
	else:
		reportChoice = request.GET['report']
	return render(request, 'stats/locations.html', { 'bubble_chart': BubbleChart(), 'leagueChoice': leagueChoice, 'season1Choice': season1Choice, 'season2Choice':season2Choice, 'positionChoice': positionChoice, 'skaterChoice': skaterChoice, 'reportChoice': reportChoice })

def getSeasons(request):
	league = request.GET['league']
	# Get appropriateleague seasons
	if int(league) == 1:
		leagueSeasons = NhlSeason.objects.all().order_by('-start_date').values('season_id')
	else:
		leagueSeasons = AhlSeason.objects.filter(Q(name__contains='Regular')).order_by('-start_date').values('season_id', 'name', 'career', 'playoff', 'start_date')
	return JsonResponse({'leagueSeasons':list(leagueSeasons)})

# Used by the location maps tool to populate skater select box based on other menu values
def getSkaters(request):
	# Get vales from menu options - used to select appropriate skater set
	league = request.GET['league']
	position = request.GET['position']
	minSeason = request.GET['minSeason']
	maxSeason = request.GET['maxSeason']

	# Get appropriateleague seasons
	if int(league) == 1:
		with connection.cursor() as cursor:
			if int(position) == 1:
				cursor.execute('SELECT * FROM nhl_locations_skaters WHERE position <> %s ORDER BY player_name', ['G', ])
			elif int(position) == 2:
				cursor.execute('SELECT * FROM nhl_locations_skaters WHERE position <> %s AND position <> %s ORDER BY player_name', ['G', 'D'])
			elif int(position) == 3:
				cursor.execute('SELECT * FROM nhl_locations_skaters WHERE position = %s ORDER BY player_name', ['D', ])
			elif int(position) == 4:
				cursor.execute('SELECT * FROM nhl_locations_skaters WHERE position = %s ORDER BY player_name', ['C', ])
			elif int(position) == 5:
				cursor.execute('SELECT * FROM nhl_locations_skaters WHERE position = %s ORDER BY player_name', ['L', ])
			elif int(position) == 6:
				cursor.execute('SELECT * FROM nhl_locations_skaters WHERE position = %s ORDER BY player_name', ['R', ])
			elif int(position) == 7:
				cursor.execute('SELECT * FROM nhl_locations_skaters WHERE position = %s OR position = %s ORDER BY player_name', ['L', 'R'])
			skaters = cursor.fetchall()
	else:
		leagueSeasons = AhlSeason.objects.filter(Q(name__contains='Regular')).order_by('-start_date').values('season_id', 'name', 'career', 'playoff', 'start_date')
	return JsonResponse({'skaters':list(skaters)})