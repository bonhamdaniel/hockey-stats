import HockeyScrape

# Gets NHL JSON Team file and adds all teams to the db
def processTeams(season):

	# Gets the json team file from the NHL api
	teamFile = HockeyScrape.getTeams('NHL', season)

	# Retrieves relevant data from the JSON team file
	teams = teamFile['teams']

	# Gets connection to specified database
	connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

	# Gets all valid seasonID's from the db
	cursor.execute('SELECT team_id FROM nhl_team')
	added = cursor.fetchall()
	for a in range(0, len(added)):
		added[a] = added[a][0]

	# Adds each team to the database
	for t in teams:
		if int(t['id']) not in added:
			print('Adding team #', t['id'])
			try:
				cursor.execute('INSERT INTO nhl_team (team_id, name, abbreviation, nickname, location, first_year, franchise_id, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (t['id'], t['name'], t['abbreviation'], t['teamName'], t['locationName'], t['firstYearOfPlay'], t['franchise']['franchiseId'], t['active']))

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

# Commits DB changes and closes the connection
connection.commit()
connection.close()

for s in seasons:
	print(s[0])
	# Calls processTeams() to add all NHL Teams to the db
	processTeams(s[0])