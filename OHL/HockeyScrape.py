import sys
import requests
import pyodbc
import psycopg2
import json

# Connects to specified database and returns connection & cursor
def getConnection(type, name):
	if type in 'access':
		driver = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
		connectionString = (driver + 'DBQ=' + name + ';')
		connection = pyodbc.connect(connectionString)
		connection.setencoding(encoding='utf-8')
	elif type in 'postgres':
		pg_conn_string = "host='localhost' dbname='" + name + "' user='postgres' password='postgres'"
		connection = psycopg2.connect(pg_conn_string)
	else:
		driver = ''

	cursor = connection.cursor()
	return connection, cursor

# Returns the user-specified gameID range from the command-line
def getGameIDs():
	startGame = int(sys.argv[1])
	if len(sys.argv) > 2:
		endGame = int(sys.argv[2])
	else:
		endGame = startGame
	return startGame, endGame

# Returns the JSON play-by-play file for the specified leage and gameID
def getPXP(league, gameID):
	if league is 'NHL':
		r = requests.get('http://statsapi.web.nhl.com/api/v1/game/' + gameID + '/feed/live')
	elif league is 'OHL':
		r = requests.get('http://cluster.leaguestat.com/feed/index.php?feed=gc&key=f109cf290fcf50d4&client_code=ohl&game_id=' + str(gameID) + '&lang_code=en&fmt=json&tab=pxpverbose')
	
	if r.status_code == 200:
		pxpFile = r.json()
		return pxpFile
	else:
		return None

# Returns the JSON play-by-play file for the specified leage and gameID
def getTeams(league, season):
	if league is 'NHL':
		r = requests.get('http://statsapi.web.nhl.com/api/v1/game/' + gameID + '/feed/live')
	elif league is 'OHL':
		r = requests.get('http://cluster.leaguestat.com/feed/?feed=modulekit&view=teamsbyseason&key=f109cf290fcf50d4&fmt=json&client_code=ohl&lang=en&season_id=' + str(season) + '&fmt=json')
	
	if r.status_code == 200:
		jsonFile = r.json()
		return jsonFile
	else:
		return None

# Returns the JSON play-by-play file for the specified leage and gameID
def getSeasons(league):
	if league is 'NHL':
		r = requests.get('http://statsapi.web.nhl.com/api/v1/game/' + gameID + '/feed/live')
	elif league is 'OHL':
		r = requests.get('http://cluster.leaguestat.com/feed/?feed=modulekit&view=seasons&key=f109cf290fcf50d4&fmt=json&client_code=ohl&lang=en&league_code=&fmt=json')
	
	if r.status_code == 200:
		jsonFile = r.json()
		return jsonFile
	else:
		return None

# Returns the JSON play-by-play file for the specified leage and gameID
def getGames(league, season):
	if league is 'NHL':
		r = requests.get('http://statsapi.web.nhl.com/api/v1/game/' + gameID + '/feed/live')
	elif league is 'OHL':
		r = requests.get('http://cluster.leaguestat.com/feed/?feed=modulekit&view=schedule&key=f109cf290fcf50d4&fmt=json&client_code=ohl&lang=en&season_id=' + str(season) + '&team_id=undefined&league_code=&fmt=json')
	
	if r.status_code == 200:
		jsonFile = r.json()
		return jsonFile
	else:
		return None

# Returns the JSON play-by-play file for the specified leage and gameID
def getPlayers(league, season, team):
	if league is 'NHL':
		r = requests.get('http://statsapi.web.nhl.com/api/v1/game/' + gameID + '/feed/live')
	elif league is 'OHL':
		r = requests.get('http://cluster.leaguestat.com/feed/?feed=modulekit&view=roster&key=f109cf290fcf50d4&fmt=json&client_code=ohl&lang=en&season_id=' + str(season) + '&team_id=' + str(team) + '&fmt=json')
	
	if r.status_code == 200:
		jsonFile = r.json()
		return jsonFile
	else:
		return None

# Returns the JSON Player bio
def getPlayer(league, player):
	if league is 'NHL':
		r = requests.get('http://statsapi.web.nhl.com/api/v1/game/' + gameID + '/feed/live')
	elif league is 'OHL':
		r = requests.get('http://cluster.leaguestat.com/feed/?feed=modulekit&view=player&key=f109cf290fcf50d4&fmt=json&client_code=ohl&lang=en&player_id=' + player + '&category=profile')
	
	if r.status_code == 200:
		jsonFile = r.json()
		return jsonFile
	else:
		return None

# Returns the JSON game summary file for the specified leage and gameID
def getGameSummary(league, game):
	if league is 'NHL':
		r = requests.get('http://statsapi.web.nhl.com/api/v1/game/' + gameID + '/feed/live')
	elif league is 'OHL':
		r = requests.get('http://cluster.leaguestat.com/feed/index.php?feed=gc&key=f109cf290fcf50d4&client_code=ohl&game_id=' + str(game) + '&lang_code=en&fmt=json&tab=gamesummary')
	
	if r.status_code == 200:
		jsonFile = r.json()
		return jsonFile
	else:
		return None

# Calculates and returns the current game time
def getGameTime(period, time):
	minutes = (int(period)-1) * 20
	time = time.split(':')
	minutes += int(time[0])
	return minutes + int(time[1])/100