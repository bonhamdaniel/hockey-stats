import HockeyScrape

# Checks AHL Season JSON file, adding any seasons not already present in the DB
def processSeason():

	# Gets the json seasons file from the AHL website
	seasonFile = HockeyScrape.getSeasons('AHL')

	# Retrieves relevant data from the JSON season file
	seasons = seasonFile['SiteKit']['Seasons']

	# Gets connection to specified database
	connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

	# Gets dict of Seasons already present in the database
	cursor.execute('SELECT season_id FROM ahl_season')
	added = cursor.fetchall()
	for a in range(0, len(added)):
		added[a] = added[a][0]

	# Adds each season to the database if not already present
	for s in seasons:
		# Adds season if it is not already present in the database
		if int(s['season_id']) not in added:
			print('Adding season #', s)
			
			try:
				cursor.execute('INSERT INTO ahl_season (season_id, name, career, playoff, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s)', (s['season_id'], s['shortname'], s['career'], s['playoff'], s['start_date'], s['end_date']))

			except Exception as e:
				print(e)
		else:
			print('Season #', s['id'], 'already present in the database')

	# Commits DB canges and closes the connection
	connection.commit()
	connection.close()

# initiates the function to add any new seasons to the database at program start
processSeason()