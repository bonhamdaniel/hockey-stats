import sys
import HockeyScrape
from unidecode import unidecode

# Procsses the JSON play-by-play file for the specified game, adding each event to its appropriate db relation
def processPXP(gameID):
	try:
		# Gets the json play-by-play file
		pxpFile = HockeyScrape.getPXP('AHL', gameID)

		# Gets connection to specified database
		connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

		# Retrieves relevant data from the JSON play-by-play file
		events = pxpFile

		# Will hold players active in current game
		skaters = []
		goalies = []

		# Gets players active in current game
		homeStats = events['homeTeam']
		home = homeStats['info']['id']
		visitingStats = events['visitingTeam']
		visitor = visitingStats['info']['id']
		for hg in homeStats['goalies']:
			goalies.append([hg, home])
		for vg in visitingStats['goalies']:
			goalies.append([vg, visitor])
		for hp in homeStats['skaters']:
			skaters.append([hp, home])
		for vp in visitingStats['skaters']:
			skaters.append([vp, visitor])

		# Gets players from db
		cursor.execute('SELECT player_id FROM ahl_player')
		players = cursor.fetchall()
		for p in range(len(players)):
			players[p] = players[p][0]

		# Adds any players not already in the db
		for c in (skaters + goalies):
			if int(c[0]['info']['id']) not in players:
				# Gets JSON player bio from
				cp = HockeyScrape.getPlayer('AHL', c[0]['info']['id'])
				p = cp['info']

				if len(p) > 2:
					# Checks for, and remedies, any missing birthdates
					if p['birthDate'] == "":
						p['birthDate'] = '1900-01-01 00:00:00'

					# Checks for and remedies any missing or malformed height values
					if p['height'] == "":
						p['height'] = 0.0
					else:
						p['height'] = p['height'].replace('\'', '.')
						p['height'] = p['height'].replace('-', '.')
						p['height'] = p['height'][0:4]

					# Checks for and remedies any missing weight values
					if p['weight'] == "" or '-' in p['weight']:
						p['weight'] = 0

					# Changes 'shoots' attribute to 'catches' for goalies
					if p['position'] == "G":
						p['shoots'] = p['catches']

					# Adds player to the db
					cursor.execute('INSERT INTO ahl_player (player_id, first_name, last_name, player_name, shoots, birthplace, height, weight, birthdate, position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (c, unidecode(p['firstName'].strip()), unidecode(p['lastName'].strip()), unidecode(p['lastName'].strip()) + '.' + unidecode(p['firstName'].strip()), p['shoots'], p['birthPlace'], p['height'], p['weight'], p['birthDate'], p['position']))
		
		# Adds Skater Game Totals
		for sk in skaters:
			s = sk[0]
			team = sk[1]
			if s['info']['position'] == None:
				s['info']['position'] = ""
			if s['info']['id'] is not 0:
				cursor.execute('INSERT INTO ahl_skater_games (game_id, player_id, position, goals, assists, pims, "+/-", shots, hits, starter, status, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (str(gameID), s['info']['id'], s['info']['position'], s['stats']['goals'], s['stats']['assists'], s['stats']['penaltyMinutes'], s['stats']['plusMinus'], s['stats']['shots'], s['stats']['hits'], s['starting'], s['status'], str(team)))
		
		# Adds Goalie Game Totals
		for go in goalies:
			g = go[0]
			team = go[1]
			result = ""
			for r in (homeStats['goalieLog'] + visitingStats['goalieLog']):
				if r['info']['id'] == g['info']['id']:
					result = r['result']
			if g['stats']['timeOnIce'] == None or '-' in g['stats']['timeOnIce']:
				time = 0.0
			else:
				time = g['stats']['timeOnIce'].split(':')[0] + '.' + str(round(int(g['stats']['timeOnIce'].split(':')[1])/60*100))
			cursor.execute('INSERT INTO ahl_goalie_games (game_id, player_id, goals, assists, pims, toi, shots, goals_against, saves, starter, status, team_id, result) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (str(gameID), g['info']['id'], g['stats']['goals'], g['stats']['assists'], g['stats']['penaltyMinutes'], time, g['stats']['shotsAgainst'], g['stats']['goalsAgainst'], g['stats']['saves'], g['starting'], g['status'], str(team), result))

	except Exception as e:
		e_type, e_object, e_tb = sys.exc_info
		print(e_tb)
		input("Press Enter to continue...")

	# Closes db connection
	connection.commit()
	connection.close()

# Gets the season to process game results for from command line
startSeason, endSeason = HockeyScrape.getGameIDs()

# Gets connection to specified database
connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

# Gets dict of all games already in the db
cursor.execute('SELECT game_id FROM ahl_skater_games')
added = cursor.fetchall()
for a in range(len(added)):
	added[a] = added[a][0]

# Closes db connection
connection.commit()
connection.close()

# Loops through each specified season, processing game results
for s in range(startSeason, endSeason+1):
	print('Processing Season #', s)

	# Gets connection to specified database
	connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

	# Gets a dict of all games for the season
	cursor.execute('SELECT game_id FROM ahl_game WHERE season_id = (%s)', (str(s), ))
	games = cursor.fetchall()

	# Closes db connection
	connection.commit()
	connection.close()

	# Processes each game in the season
	for g in games:
		if int(g[0]) not in added:
			print('Processing Game #', g[0])
			processPXP(g[0])
		else:
			print('Game #', g[0], 'already processed')