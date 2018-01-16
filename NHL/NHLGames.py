import HockeyScrape

# Gets NHL JSON Game file for each NHL Season in the db and adds all games to the db
def processGames(season, teams):

	# Gets the json game file from the NHL api
	gameFile = HockeyScrape.getGames('NHL', season)

	# Retrieves relevant data from the JSON game file
	games = []
	dates = gameFile['dates']
	for d in dates:
		for game in d['games']:
			games.append(game)

	# Gets connection to specified database
	connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

	# Adds each game to the database
	for g in games:
		if 'Final' in g['status']['abstractGameState']:
			print('Adding game #', g['gamePk'])
			if int(g['teams']['away']['team']['id']) not in teams:
				HockeyScrape.addTeam('NHL', g['teams']['away']['team']['id'], cursor)
				teams.append(int(g['teams']['away']['team']['id']))
			if int(g['teams']['home']['team']['id']) not in teams:
				HockeyScrape.addTeam('NHL', g['teams']['home']['team']['id'], cursor)
				teams.append(int(g['teams']['home']['team']['id']))

			try:
				cursor.execute('INSERT INTO nhl_game (game_id, season_id, type, game_date, away_team, away_goals, home_team, home_goals, venue) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (g['gamePk'], g['season'], g['gameType'], g['gameDate'], g['teams']['away']['team']['id'], g['teams']['away']['score'], g['teams']['home']['team']['id'], g['teams']['home']['score'], g['venue']['name']))

			except Exception as e:
				print(e)

	# Commits DB changes and closes the connection
	connection.commit()
	connection.close()

# Gets connection to specified database
connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

# Gets all valid seasonID's from the db
cursor.execute('SELECT season_id FROM nhl_season')
seasons = cursor.fetchall()

# Gets all valid seasonID's from the db
cursor.execute('SELECT team_id FROM nhl_team')
teams = cursor.fetchall()
for t in range(0, len(teams)):
	teams[t] = teams[t][0]

# Commits DB changes and closes the connection
connection.commit()
connection.close()

for s in seasons:
	print(s[0])
	# Calls processGames() to add all NHL games to the db
	processGames(s[0], teams)