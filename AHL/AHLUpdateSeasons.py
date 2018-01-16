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
		print('Adding season #', s)
			
		try:
			cursor.execute('UPDATE ahl_season SET start_date = (%s) WhERE season_id = (%s)', (s['start_date'], s['season_id']))

		except Exception as e:
			print(e)

	# Commits DB canges and closes the connection
	connection.commit()
	connection.close()

# initiates the function to add any new seasons to the database at program start
processSeason()