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

		# Process Referees
		officials = []
		referees = events['referees']
		linesmen = events['linesmen']
		for r in referees:
			officials.append(r['lastName'] + '.' + r['firstName'])
		for i in range(len(referees), 2):
			officials.append('null')
		for l in linesmen:
			officials.append(l['lastName'] + '.' + l['firstName'])
		for i in range(len(linesmen), 2):
			officials.append('null')
		cursor.execute('INSERT INTO ahl_official (game_id, referee1, referee2, linesman1, linesman2) VALUES (%s, %s, %s, %s, %s)', (str(gameID), officials[0], officials[1], officials[2], officials[3]))

		# Gets players from db
		cursor.execute('SELECT player_id FROM ahl_player')
		players = cursor.fetchall()
		for p in range(len(players)):
			players[p] = players[p][0]

		# Will hold players active in current game
		current = []

		# Gets players active in current game
		homeStats = events['homeTeam']
		visitingStats = events['visitingTeam']
		for hg in homeStats['goalies']:
			current.append(hg['info']['id'])
		for vg in visitingStats['goalies']:
			current.append(vg['info']['id'])
		for hp in homeStats['skaters']:
			current.append(hp['info']['id'])
		for vp in visitingStats['skaters']:
			current.append(vp['info']['id'])

		# Adds any players not already in the db
		for c in current:
			if int(c) not in players:
				# Gets JSON player bio from
				cp = HockeyScrape.getPlayer('AHL', c)
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
		
		# Process three stars
		mvps = events['mostValuablePlayers']
		for i in range(len(mvps), 3):
			mvps.append({'player':{'info':{'id':0}}})
		cursor.execute('INSERT INTO ahl_stars(game_id, first, second, third) VALUES (%s, %s, %s, %s)', (str(gameID), mvps[0]['player']['info']['id'], mvps[1]['player']['info']['id'], mvps[2]['player']['info']['id']))

		# Keeps track of the number of penalties taken in the game, used for identification purposes
		shootoutShots = 0

		# Processes a shootout, if necessary
		if events['hasShootout'] == True:
			shootout = events['shootoutDetails']
			for e in shootout['homeTeamShots']:
				shootoutShots += 1
				if e['isGoal'] == True:
					isGoal = 1
				else:
					isGoal = 0
				if e['isGameWinningGoal'] == True:
					isWinner = 1
				else:
					isWinner = 0
				cursor.execute('INSERT INTO ahl_shootout (game_id, shooter, shooter_team, goalie, goalie_team, home, goal, winning_goal, s_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (str(gameID), e['shooter']['id'], e['shooterTeam']['id'], e['goalie']['id'], events['visitingTeam']['info']['id'], 1, isGoal, isWinner, str(shootoutShots)))
			for e in shootout['visitingTeamShots']:
				shootoutShots += 1
				if e['isGoal'] == True:
					isGoal = 1
				else:
					isGoal = 0
				if e['isGameWinningGoal'] == True:
					isWinner = 1
				else:
					isWinner = 0
				cursor.execute('INSERT INTO ahl_shootout (game_id, shooter, shooter_team, goalie, goalie_team, home, goal, winning_goal, s_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (str(gameID), e['shooter']['id'], e['shooterTeam']['id'], e['goalie']['id'], events['homeTeam']['info']['id'], 0, isGoal, isWinner, str(shootoutShots)))

		# Process Team Totals 
		h = events['homeTeam']['stats']
		v = events['visitingTeam']['stats']
		cursor.execute('INSERT INTO ahl_team_game_totals (game_id, home_shots, home_hits, home_ppg, home_ppo, home_goals, home_assists, home_pims, home_penalties, visitor_shots, visitor_hits, visitor_ppg, visitor_ppo, visitor_goals, visitor_assists, visitor_pims, visitor_penalties) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (str(gameID), h['shots'], h['hits'], h['powerPlayGoals'], h['powerPlayOpportunities'], h['goalCount'], h['assistCount'], h['penaltyMinuteCount'], h['infractionCount'], v['shots'], v['hits'], v['powerPlayGoals'], v['powerPlayOpportunities'], v['goalCount'], v['assistCount'], v['penaltyMinuteCount'], v['infractionCount']))

		# Process Coaches
		coaches = []
		homeCoaches = events['homeTeam']['coaches']
		visitingCoaches = events['visitingTeam']['coaches']
		for r in homeCoaches:
			coaches.append(r['lastName'] + '.' + r['firstName'])
		for i in range(len(homeCoaches), 5):
			coaches.append('null')
		for l in visitingCoaches:
			coaches.append(l['lastName'] + '.' + l['firstName'])
		for i in range(len(visitingCoaches), 5):
			coaches.append('null')
		cursor.execute('INSERT INTO ahl_coaches (game_id, home_head, home_a1, home_a2, home_a3, home_a4, visitor_head, visitor_a1, visitor_a2, visitor_a3, visitor_a4) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (str(gameID), coaches[0], coaches[1], coaches[2], coaches[3], coaches[4], coaches[5], coaches[6], coaches[7], coaches[8], coaches[9]))

		# Keeps track of the current score
		homeGoals = 0
		awayGoals = 0

		# Keeps track of the number of penalties taken in the game, used for identification purposes
		penaltyNum = 0

		# Process Goals and Assists
		periods = events['periods']
		for p in periods:
			period = p['info']['id']
			goals = p['goals']
			
			for g in goals:
				if g['team']['id'] == events['homeTeam']['info']['id']:
					home = 1
					homeGoals += 1
				else:
					home = 0
					awayGoals += 1
				time = HockeyScrape.getGameTime(period, g['time'])
				a = []
				for ass in g['assists']:
					a.append(ass['id'])
				for i in range(len(a), 2):
					a.append(0)
				plus = ["0", "0", "0", "0", "0", "0"]
				duplicates = 0
				for pen in range(0, len(g['plus_players'])):
					if g['plus_players'][pen]['id'] not in plus and pen-duplicates < len(plus):
						plus[pen-duplicates] = g['plus_players'][pen]['id']
					else:
						duplicates += 1
				minus = ["0", "0", "0", "0", "0", "0"]
				for m in range(0, len(g['minus_players'])):
					minus[m] = g['minus_players'][m]['id']
				sql = 'INSERT INTO ahl_goal (game_id, period, time, team, scorer, a1, a2, pp, en, ps, sh, gf1, gf2, gf3, gf4, gf5, gf6, ga1, ga2, ga3, ga4, ga5, ga6, home, home_goals, visitor_goals) VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
				params = (str(gameID), period, time, g['team']['id'], g['scoredBy']['id'], a[0], a[1], g['properties']['isPowerPlay'], g['properties']['isEmptyNet'], g['properties']['isPenaltyShot'], g['properties']['isShortHanded'], plus[0], plus[1], plus[2], plus[3], plus[4], plus[5], minus[0], minus[1], minus[2], minus[3], minus[4], minus[5], home, homeGoals, awayGoals)
				cursor.execute(sql, params)

			penalties = p['penalties']
			for pen in penalties:
				penaltyNum += 1
				if pen['againstTeam']['id'] == events['homeTeam']['info']['id']:
					home = 1
				else:
					home = 0
				if pen['isPowerPlay'] == 'true' or pen['isPowerPlay'] == True:
					pen['isPowerPlay'] = 1
				if pen['isPowerPlay'] == 'false' or pen['isPowerPlay'] == False:
					pen['isPowerPlay'] = 0
				if pen['takenBy'] == None:
					pen['takenBy']= {'id': 0}
				time = HockeyScrape.getGameTime(period, pen['time'])
				cursor.execute('INSERT INTO ahl_penalty (game_id, period, time, player, team, pp, home, mins, description, pen_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (str(gameID), period, time, pen['takenBy']['id'], pen['againstTeam']['id'], pen['isPowerPlay'], home, pen['minutes'], pen['description'], str(penaltyNum)))
		
		# Adds gameID to ohl_pxp, marking it as processed
		cursor.execute('INSERT INTO ahl_pxp (game_id) VALUES (%s)', (str(gameID), ))

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
cursor.execute('SELECT game_id FROM ahl_pxp')
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