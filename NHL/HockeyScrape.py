import sys
import requests
import pyodbc
import psycopg2
import json
from unidecode import unidecode

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
		r = requests.get('http://statsapi.web.nhl.com/api/v1/game/' + str(gameID) + '/feed/live')
	elif league is 'OHL':
		r = requests.get('http://cluster.leaguestat.com/feed/index.php?feed=gc&key=f109cf290fcf50d4&client_code=ohl&game_id=' + str(gameID) + '&lang_code=en&fmt=json&tab=pxpverbose')
	elif league is 'AHL':
		r = requests.get('https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=gameSummary&game_id=' + str(gameID) + '&key=50c2cd9b5e18e390&client_code=ahl&lang=en')
	
	if r.status_code == 200:
		if league is 'AHL':
			jsonFile = json.loads(r.text[1:-1])
		else:
			jsonFile = r.json()
		return jsonFile
	else:
		return None

# Returns the JSON Franchise file for the specified leage
def getFranchises(league):
	if league is 'NHL':
		r = requests.get('https://statsapi.web.nhl.com/api/v1/franchises')

	if r.status_code == 200:
		jsonFile = r.json()
		return jsonFile
	else:
		return None

# Returns the JSON play-by-play file for the specified leage and gameID
def getTeams(league, season):
	if league is 'NHL':
		r = requests.get('https://statsapi.web.nhl.com/api/v1/teams?season=' + str(season))
	elif league is 'OHL':
		r = requests.get('http://cluster.leaguestat.com/feed/?feed=modulekit&view=teamsbyseason&key=f109cf290fcf50d4&fmt=json&client_code=ohl&lang=en&season_id=' + str(season) + '&fmt=json')
	elif league is 'AHL':
		r = requests.get('https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=teamsForSeason&season=' + str(season) + '&key=50c2cd9b5e18e390&client_code=ahl&site_id=1')
	
	if r.status_code == 200:
		if league is 'AHL':
			jsonFile = json.loads(r.text[1:-1])
		else:
			jsonFile = r.json()
		return jsonFile
	else:
		return None

# Returns the JSON play-by-play file for the specified leage and gameID
def getSeasons(league):
	if league is 'NHL':
		r = requests.get('https://statsapi.web.nhl.com/api/v1/seasons')
	elif league is 'OHL':
		r = requests.get('http://cluster.leaguestat.com/feed/?feed=modulekit&view=seasons&key=f109cf290fcf50d4&fmt=json&client_code=ohl&lang=en&league_code=&fmt=json')
	elif league is 'AHL':
		r = requests.get('https://lscluster.hockeytech.com/feed/index.php?feed=modulekit&view=seasons&key=50c2cd9b5e18e390&client_code=ahl&site_id=1&league_id=4')

	if r.status_code == 200:
		jsonFile = r.json()
		return jsonFile
	else:
		return None

# Returns the JSON play-by-play file for the specified leage and gameID
def getGames(league, season):
	if league is 'NHL':
		r = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?season=' + str(season))
	elif league is 'OHL':
		r = requests.get('http://cluster.leaguestat.com/feed/?feed=modulekit&view=schedule&key=f109cf290fcf50d4&fmt=json&client_code=ohl&lang=en&season_id=' + str(season) + '&team_id=undefined&league_code=&fmt=json')
	elif league is 'AHL':
		r = requests.get('https://lscluster.hockeytech.com/feed/index.php?feed=modulekit&view=schedule&season_id=' + str(season) + '&key=50c2cd9b5e18e390&client_code=ahl&fmt=json')
	
	if r.status_code == 200:
		jsonFile = r.json()
		return jsonFile
	else:
		return None

# Returns the JSON play-by-play file for the specified leage and gameID
def getPlayers(league, season, team):
	if league is 'NHL':
		r = requests.get('https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster,roster.person&season=' + str(season))
	elif league is 'OHL':
		r = requests.get('http://cluster.leaguestat.com/feed/?feed=modulekit&view=roster&key=f109cf290fcf50d4&fmt=json&client_code=ohl&lang=en&season_id=' + str(season) + '&team_id=' + str(team) + '&fmt=json')
	elif league is 'AHL':
		r = requests.get('https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=roster&season_id=' + str(season) + '&team_id=' + str(team) + '&key=50c2cd9b5e18e390&client_code=ahl&site_id=1')
	
	if r.status_code == 200:
		if league is 'AHL':
			jsonFile = json.loads(r.text[1:-1])
		else:
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
	elif league is 'AHL':
		r = requests.get('https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=player&player_id=' + str(player) + '&key=50c2cd9b5e18e390&client_code=ahl&fmt=json')
	
	if r.status_code == 200:
		if league is 'AHL':
			jsonFile = json.loads(r.text[1:-1])
		else:
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

# Returns the JSON game summary file for the specified leage and gameID
def getShifts(league, game):
	if league is 'NHL':
		r = requests.get('http://www.nhl.com/stats/rest/shiftcharts?cayenneExp=gameId=' + str(game))
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

# Adds the requested team to its appropriate league relation in the db
def addTeam(league, team, cursor):
	if league is 'NHL':
		r = requests.get('http://statsapi.web.nhl.com/api/v1/teams/' + str(team))
	
	if r.status_code == 200:
		t = r.json()['teams'][0]
		print('Adding team #', t['id'])
		try:
			cursor.execute('INSERT INTO nhl_team (team_id, name, abbreviation, nickname, location, first_year, franchise_id, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (t['id'], t['name'], t['abbreviation'], t['teamName'], t['locationName'], str(-1), str(-1), t['active']))

		except Exception as e:
			print(e)
	else:
		return

# Gets all players already added to the DB for the specified league
def getDBPlayers(league, cursor):
	if league is 'NHL':
		cursor.execute('SELECT player_id FROM nhl_player')
		players = cursor.fetchall()
		for p in range(0, len(players)):
			players[p] = players[p][0]
		return players

def addNHLPlayer(pl, cursor):
	if 'birthStateProvince' not in pl:
		pl['birthStateProvince'] = ''
	if 'birthCountry' not in pl:
		pl['birthCountry'] = ''
	if 'shootsCatches' not in pl:
		pl['shootsCatches'] = ''
	if 'birthCity' not in pl:
		pl['birthCity'] = ''
	if 'birthDate' not in pl:
		pl['birthDate'] = '1900-01-01'
	cursor.execute('INSERT INTO nhl_player (player_id, first_name, last_name, birthdate, shoots, player_name, town, province, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (pl['id'], unidecode(pl['firstName'].strip()), unidecode(pl['lastName'].strip()), pl['birthDate'], pl['shootsCatches'], unidecode(pl['lastName'].strip()) + '.' + unidecode(pl['firstName'].strip()), pl['birthCity'], pl['birthStateProvince'], pl['birthCountry']))

def convertTime(rawTime):
	time = rawTime.split(':')[0] + '.' + rawTime.split(':')[1]
	return time