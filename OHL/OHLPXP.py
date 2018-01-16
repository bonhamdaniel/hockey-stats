import sys
import HockeyScrape
from unidecode import unidecode

# Procsses the JSON play-by-play file for the specified game, adding each event to its appropriate db relation
def processPXP(gameID):
	# Gets the json play-by-play file
	pxpFile = HockeyScrape.getPXP('OHL', gameID)

	# Retrieves relevant data from the JSON play-by-play file
	events = pxpFile['GC']['Pxpverbose']

	# Gets connection to specified database
	connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

	# Gets players from db
	cursor.execute('SELECT player_id FROM ohl_player')
	players = cursor.fetchall()
	for p in range(len(players)):
		players[p] = players[p][0]

	# Gets game summary file
	gameSummary = HockeyScrape.getGameSummary('OHL', gameID)['GC']['Gamesummary']
	homeTeam = gameSummary['meta']['home_team']
	visitingTeam = gameSummary['meta']['visiting_team']

	# Will hold players active in current game
	current = []

	# Gets players active in current game
	homeGoalies = gameSummary['home_team_lineup']['goalies']
	for hg in homeGoalies:
		current.append(hg['player_id'])
	visitingGoalies = gameSummary['visitor_team_lineup']['goalies']
	for vg in visitingGoalies:
		current.append(vg['player_id'])
	homePlayers = gameSummary['home_team_lineup']['players']
	for hp in homePlayers:
		current.append(hp['player_id'])
	visitingPlayers = gameSummary['visitor_team_lineup']['players']
	for vp in visitingPlayers:
		current.append(vp['player_id'])

	# Adds any players not already in the db
	for c in current:
		if int(c) not in players:
			# Gets JSON player bio from
			cp = HockeyScrape.getPlayer('OHL', c)
			p = cp['SiteKit']['Player']

			if len(p) > 2:
				# Checks for, and remedies, any missing birthdates
				if p['birthdate'] == "":
					p['birthdate'] = '1900-01-01 00:00:00'

				# Checks for and remedies any missing or malformed height values
				if p['height'] == "":
					p['height'] = 0.0
				else:
					p['height'] = p['height'].replace('\'', '.')
					p['height'] = p['height'].replace('-', '.')
					p['height'] = p['height'][0:4]

				# Checks for and remedies any missing weight values
				if p['weight'] == "":
					p['weight'] = 0

				# Adds player to the db
				cursor.execute('INSERT INTO ohl_player (player_id, first_name, last_name, player_name, shoots, town, province, country, height, weight, birthdate, position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (cp['SiteKit']['Parameters']['player_id'], unidecode(p['first_name'].strip()), unidecode(p['last_name'].strip()), unidecode(p['last_name'].strip()) + '.' + unidecode(p['first_name'].strip()), p['shoots'], p['hometown'], p['homeprov'], p['homecntry'], p['height'], p['weight'], p['birthdate'], p['position']))
					

	# Keeps track of the current score
	homeGoals = 0
	awayGoals = 0

	# Keeps track of the number of shots taken in the game, used for identification purposes
	shotNum = 0

	# Keeps track of the number of penalties taken in the game, used for identification purposes
	penaltyNum = 0

	# Keeps track of the number of faceoffs taken in the game, used for identification purposes
	faceoffNum = 0

	# Processes each individual event in the pxp file
	for e in events:
		try:
			event = e['event']
			if event == 'goal':
				if e['home'] == '1':
					homeGoals += 1
				else:
					awayGoals += 1
				time = HockeyScrape.getGameTime(e['period_id'], e['time_formatted'])
				if e['assist1_player_id'] == "":
					e['assist1_player_id'] = "0"
				if e['assist2_player_id'] == "":
					e['assist2_player_id'] = "0"
				plus = ["0", "0", "0", "0", "0", "0"]
				#print("Plus:", e['plus'])
				for p in range(0, len(e['plus'])):
					plus[p] = e['plus'][p]['player_id']
				#print("Plus:", plus)

				minus = ["0", "0", "0", "0", "0", "0"]
				for m in range(0, len(e['minus'])):
					minus[m] = e['minus'][m]['player_id']
				#print(gameID, e['period_id'], time, e['team_id'], e['goal_player_id'], e['assist1_player_id'], e['assist2_player_id'], e['x_location'], e['y_location'], e['location_set'], e['power_play'], e['empty_net'], e['penalty_shot'], e['short_handed'], plus[0], plus[1], plus[2], plus[3], plus[4], plus[5], minus[0], minus[1], minus[2], minus[3], minus[4], minus[5], e['home'], str(homeGoals), str(awayGoals))
				sql = 'INSERT INTO ohl_goal (game_id, period, time, team, scorer, a1, a2, x, y, location, pp, en, ps, sh, gf1, gf2, gf3, gf4, gf5, gf6, ga1, ga2, ga3, ga4, ga5, ga6, home, home_goals, visitor_goals) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
				params = (str(gameID), e['period_id'], time, e['team_id'], e['goal_player_id'].strip(), e['assist1_player_id'].strip(), e['assist2_player_id'].strip(), e['x_location'], e['y_location'], e['location_set'], e['power_play'], e['empty_net'], e['penalty_shot'], e['short_handed'], plus[0], plus[1], plus[2], plus[3], plus[4], plus[5], minus[0], minus[1], minus[2], minus[3], minus[4], minus[5], e['home'], str(homeGoals), str(awayGoals))
				cursor.execute(sql, params)
			elif event == 'goalie_change':
				time = HockeyScrape.getGameTime(e['period_id'], e['time'])
				cursor.execute('INSERT INTO ohl_goalie_change (game_id, goalie_in, goalie_out, period, time, team, home_goals, visitor_goals) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (str(gameID), e['goalie_in_id'], e['goalie_out_id'], e['period_id'], time, e['team_id'], str(homeGoals), str(awayGoals)))
			elif event == 'faceoff':
				if e['player_home']['team_id'] == None:
					e['player_home']['team_id'] = homeTeam
				if e['player_visitor']['team_id'] == None:
					e['player_visitor']['team_id'] = visitingTeam
				faceoffNum += 1
				time = HockeyScrape.getGameTime(e['period'], e['time_formatted'])
				cursor.execute('INSERT INTO ohl_faceoff (game_id, period, time, home_player, visitor_player, home_win, location, x, y, home_team, visitor_team, home_goals, visitor_goals, fo_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (str(gameID), e['period'], time, e['home_player_id'], e['visitor_player_id'], e['home_win'], e['location_id'], e['x_location'], e['y_location'], e['player_home']['team_id'], e['player_visitor']['team_id'], str(homeGoals), str(awayGoals), str(faceoffNum)))
			elif event == 'shot':
				shotNum += 1
				time = HockeyScrape.getGameTime(e['period_id'], e['time_formatted'])
				cursor.execute('INSERT INTO ohl_shot (game_id, shooter, goalie, home, team, period, time, x, y, shot, quality, goal, opponent, home_goals, visitor_goals, shot_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (str(gameID), e['player_id'], e['goalie_id'], e['home'], e['team_id'], e['period_id'], time, e['x_location'], e['y_location'], e['shot_type'], e['quality'], e['game_goal_id'], e['goalie_team_id'], str(homeGoals), str(awayGoals), str(shotNum)))
			elif event == 'penaltyshot':
				time = HockeyScrape.getGameTime(e['period_id'], e['time'])
				cursor.execute('INSERT INTO ohl_penaltyshot (game_id, shooter, shooter_team, goalie, goalie_team, home, goal, time, period) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (str(gameID), e['player_id'], e['team_id'], e['goalie_id'], e['goalie']['team_id'], e['home'], e['game_goal_id'], time, e['period_id']))
			elif event == 'penalty':
				penaltyNum += 1
				time = HockeyScrape.getGameTime(e['period_id'], e['time_off_formatted'])
				if e['penalty_shot'] == "":
					e['penalty_shot'] = 0
				if e['bench'] == "":
					e['bench'] = 0
				cursor.execute('INSERT INTO ohl_penalty (game_id, period, time, player, team, offence, pp, ps, bench, home, mins, description, class, home_goals, visitor_goals, pen_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (str(gameID), e['period_id'], time, e['player_id'], e['team_id'], e['offence'], e['pp'], e['penalty_shot'], e['bench'], e['home'], e['minutes'], e['penalty_class'], e['lang_penalty_description'], str(homeGoals), str(awayGoals), str(penaltyNum)))
			elif event == 'shootout':
				if e['goal'] == "":
					e['goal'] = 0
				cursor.execute('INSERT INTO ohl_shootout (game_id, shooter, shooter_team, goalie, goalie_team, home, shot_order, shot, goal, winning_goal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (str(gameID), e['player_id'], e['team_id'], e['goalie_id'], e['goalie_info']['team_id'], e['home'], e['shot_order'], e['s'], e['goal'], e['winning_goal']))
			else:
				print(event)
		except Exception as e:
			print(e.args)
			print(e)
			input("Press Enter to continue...")

	# Adds gameID to ohl_pxp, marking it as processed
	cursor.execute('INSERT INTO ohl_pxp (game_id) VALUES (%s)', (str(gameID), ))

	# Closes db connection
	connection.commit()
	connection.close()

# Gets the season to process game results for from command line
startSeason, endSeason = HockeyScrape.getGameIDs()

# Gets connection to specified database
connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

# Gets dict of all games already in the db
cursor.execute('SELECT game_id FROM ohl_pxp')
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
	cursor.execute('SELECT game_id FROM ohl_game WHERE season_id = (%s)', (str(s), ))
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