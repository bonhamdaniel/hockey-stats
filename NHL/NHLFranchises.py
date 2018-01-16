import HockeyScrape

# Gets NHL JSON Franchise file and adds all franchises to the db
def processFranchises():

	# Gets the json franchise file from the NHL api
	franchiseFile = HockeyScrape.getFranchises('NHL')

	# Retrieves relevant data from the JSON franchise file
	franchises = franchiseFile['franchises']

	# Gets connection to specified database
	connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

	# Adds each franchise to the database
	for f in franchises:
		print('Adding franchise #', f['franchiseId'])
		try:
			cursor.execute('INSERT INTO nhl_franchise (franchise_id, first_season, recent_team, team_name, location) VALUES (%s, %s, %s, %s, %s)', (f['franchiseId'], f['firstSeasonId'], f['mostRecentTeamId'], f['teamName'], f['locationName']))

		except Exception as e:
			print(e)

	# Commits DB changes and closes the connection
	connection.commit()
	connection.close()


# Calls processFranchises() to add all NHL Franchises to the db
processFranchises()