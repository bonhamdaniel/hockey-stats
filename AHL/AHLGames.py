import HockeyScrape

# Processes given season, adding any games missing from the ahl_game relation in the AHL db
def processSeason(season, added):
	# Gets the json games file for the given season
	gameFile = HockeyScrape.getGames('AHL', season)

	# Retrieves game data from the JSON season file
	games = gameFile['SiteKit']['Schedule']

	# Gets connection to specified database
	connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

	# Adds each missing game to the database
	for g in games:
		try:
			# Checks for completed games that are not yet in the db
			if int(g['game_id']) not in added and 'Final' in g['game_status']:

				# Adds game to the db
				cursor.execute('INSERT INTO ahl_game (game_id, season_id, game_date, home_team, visiting_team, home_goals, visiting_goals, period, overtime, shootout, attendance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (g['game_id'], g['season_id'], g['date_played'], g['home_team'], g['visiting_team'], g['home_goal_count'], g['visiting_goal_count'], g['period'], g['overtime'], g['shootout'], g['attendance']))
				added.append(int(g['game_id']))
		except Exception as e:
			print(e)

	# Commits DB changes and closes the connection
	connection.commit()
	connection.close()

# Gets the games to parse from the command line
startSeason, endSeason = HockeyScrape.getGameIDs()

# Gets connection to specified database
connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

# Gets dict of seasons present in db
cursor.execute('SELECT season_id FROM ahl_season')
seasons = cursor.fetchall()
for s in range(0, len(seasons)):
	seasons[s] = str(seasons[s]).split(',')[0]
	seasons[s] = int(seasons[s][1:])

# Gets dict of games already present in the db
cursor.execute('SELECT game_id FROM ahl_game')
added = cursor.fetchall()
for a in range(0, len(added)):
	added[a] = added[a][0]

# Closes db connection
connection.commit()
connection.close()

# Loops through all seasons in db, checking for missing games - adding if necessary
for s in range(startSeason, endSeason+1):
	# Checks if seasonID is valid
	if s in seasons:
		print('Processing Season #', s)
		processSeason(s, added)
	else:
		print('Invalid SeasonID')