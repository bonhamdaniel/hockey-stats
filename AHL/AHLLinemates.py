import HockeyScrape

# Checks AHL Season JSON file, adding any seasons not already present in the DB
def processOnIce():

	# Gets connection to specified database
	connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

	# Gets Player.Season pairs from DB
	cursor.execute('SELECT player_id, season_id FROM ahl_skater_gp')
	playerSeasons = cursor.fetchall()

	# Loops through each playe season, calculating linemate scores and adding them to the DB
	for ps in playerSeasons:
		print(ps)
		esLinemates = []
		esOpponents = []
		goalsFor = 0
		goalsAgainst = 0

		# Gets Linemates from GFs
		cursor.execute('SELECT gf1, gf2, gf3, gf4, gf5 FROM ahl_goal JOIN ahl_game ON ahl_goal.game_id = ahl_game.game_id WHERE pp = 0 AND sh = 0 AND en = 0 AND gf6 = 0 AND season_id = (%s) AND (gf1 = (%s) OR gf2 = (%s) OR gf3 = (%s) OR gf4 = (%s) OR gf5 = (%s))', (str(ps[1]), str(ps[0]), str(ps[0]), str(ps[0]), str(ps[0]), str(ps[0])))
		linemates = cursor.fetchall()
		# Gets Opponents from GFs
		cursor.execute('SELECT ga1, ga2, ga3, ga4, ga5 FROM ahl_goal JOIN ahl_game ON ahl_goal.game_id = ahl_game.game_id WHERE pp = 0 AND sh = 0 AND en = 0 AND gf6 = 0 AND season_id = (%s) AND (gf1 = (%s) OR gf2 = (%s) OR gf3 = (%s) OR gf4 = (%s) OR gf5 = (%s))', (str(ps[1]), str(ps[0]), str(ps[0]), str(ps[0]), str(ps[0]), str(ps[0])))
		opponents = cursor.fetchall()
		
		for l in linemates:
			goalsFor += 1
			for t in l:
				if t != 0:
					esLinemates.append(t)
		for o in opponents:
			for t in o:
				if t != 0:
					esOpponents.append(t)
		
		# Gets Linemates from GAs
		cursor.execute('SELECT gf1, gf2, gf3, gf4, gf5 FROM ahl_goal JOIN ahl_game ON ahl_goal.game_id = ahl_game.game_id WHERE pp = 0 AND sh = 0 AND en = 0 AND gf6 = 0 AND season_id = (%s) AND (ga1 = (%s) OR ga2 = (%s) OR ga3 = (%s) OR ga4 = (%s) OR ga5 = (%s))', (str(ps[1]), str(ps[0]), str(ps[0]), str(ps[0]), str(ps[0]), str(ps[0])))
		opponents = cursor.fetchall()
		# Gets Opponents from GAs
		cursor.execute('SELECT ga1, ga2, ga3, ga4, ga5 FROM ahl_goal JOIN ahl_game ON ahl_goal.game_id = ahl_game.game_id WHERE pp = 0 AND sh = 0 AND en = 0 AND gf6 = 0 AND season_id = (%s) AND (ga1 = (%s) OR ga2 = (%s) OR ga3 = (%s) OR ga4 = (%s) OR ga5 = (%s))', (str(ps[1]), str(ps[0]), str(ps[0]), str(ps[0]), str(ps[0]), str(ps[0])))
		linemates = cursor.fetchall()
		
		for l in linemates:
			goalsAgainst += 1
			for t in l:
				if t != 0 and t != ps[1]:
					esLinemates.append(t)
		for o in opponents:
			for t in o:
				if t != 0:
					esOpponents.append(t)

		teammates = 0
		for esl in esLinemates:
			esTotal = 0
			cursor.execute('SELECT \"ES GF-GA\" FROM ahl_onice_rates JOIN ahl_season ON ahl_onice_rates."SEASON" = ahl_season.name JOIN ahl_player ON ahl_onice_rates."PLAYER" = ahl_player.player_name WHERE season_id = (%s) AND player_id = (%s)', (str(ps[1]), str(esl)))
			result = cursor.fetchall()
			esTotal += result[0][0]
			if len(esLinemates) > 0:
				teammates = esTotal/len(esLinemates)
			else:
				teammates = 0

		opponents = 0
		for esl in esOpponents:
			esTotal = 0
			cursor.execute('SELECT \"ES GF-GA\" FROM ahl_onice_rates JOIN ahl_season ON ahl_onice_rates."SEASON" = ahl_season.name JOIN ahl_player ON ahl_onice_rates."PLAYER" = ahl_player.player_name WHERE season_id = (%s) AND player_id = (%s)', (str(ps[1]), str(esl)))
			result = cursor.fetchall()
			esTotal += result[0][0]
			if len(esOpponents) > 0:
				opponents = esTotal/len(esOpponents)
			else:
				opponents = 0

		cursor.execute('INSERT INTO ahl_line_comp (player_id, season_id, es_line, es_comp) VALUES (%s, %s, %s, %s)', (str(ps[0]), str(ps[1]), teammates, opponents))
		connection.commit()
		#print(ps[0], ps[1], goalsFor, goalsAgainst, teammates, opponents)

	# Commits DB canges and closes the connection
	connection.commit()
	connection.close()

# initiates the function to add any new seasons to the database at program start
processOnIce()