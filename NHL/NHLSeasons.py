import HockeyScrape

# Gets NHL JSON Season file and adds all seasons to the db
def processSeasons():

	# Gets the json season file from the NHL api
	seasonFile = HockeyScrape.getSeasons('NHL')

	# Retrieves relevant data from the JSON team file
	seasons = seasonFile['seasons']

	# Gets connection to specified database
	connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

	# Adds each team to the database
	for s in seasons:
		print('Adding season #', s['seasonId'])
		try:
			cursor.execute('INSERT INTO nhl_season (season_id, start_date, end_date, games, ties, olympics, conferences, divisions, wild_cards) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (s['seasonId'], s['regularSeasonStartDate'], s['regularSeasonEndDate'], s['numberOfGames'], s['tiesInUse'], s['olympicsParticipation'], s['conferencesInUse'], s['divisionsInUse'], s['wildCardInUse']))

		except Exception as e:
			print(e)

	# Commits DB changes and closes the connection
	connection.commit()
	connection.close()


# Calls processSeasons() to add all NHL Seasons to the db
processSeasons()