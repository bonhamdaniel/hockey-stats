import HockeyScrape

# Checks OHL Teams JSON file for each relevant season, adding teams to the db
def processSeason(seasonID):

	# Gets the json team file for the current season from the OHL website
	teamFile = HockeyScrape.getTeams('OHL', seasonID)

	# Retrieves relevant data from the JSON season/team file
	teams = teamFile['SiteKit']['Teamsbyseason']

	# Gets connection to specified database
	connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

	# Checks if seasonID is valid - only want to add teams for seasons already in the db
	cursor.execute('SELECT * FROM ohl_season WHERE season_id = (%s)', (str(seasonID), ))
	season = cursor.fetchall()

	# Continues to process team file if the seasonID is valid
	if len(season) > 0:
		# Gets dict of teams already present in the database for the given season
		cursor.execute('SELECT team_id FROM ohl_team WHERE season_id = (%s)', (str(seasonID),))
		added = cursor.fetchall()
		for a in range(0, len(added)):
			added[a] = added[a][0]

		# Adds each season/team to the database
		for t in teams:
			# Adds team if it is not already present in the database
			if int(t['id']) not in added:
				print('Adding team #', t['id'], 'to season #', seasonID)
				try:
					cursor.execute('INSERT INTO ohl_team (season_id, team_id, name, code, city, nickname) VALUES (%s, %s, %s, %s, %s, %s)', (str(seasonID), t['id'], t['name'], t['code'], t['city'], t['nickname']))

				except KeyError as e:
					print(e)
			else:
				print('Team #', t['id'], 'already present in the database for Season #', seasonID)

	# Commits DB canges and closes the connection
	connection.commit()
	connection.close()


# Gets the seasons to process from the command line
startSeason, endSeason = HockeyScrape.getGameIDs()

# Calls processSeason() function for each specified seasonID, adding season/team pairs to the db
for s in range(startSeason, endSeason+1):
	print('Processing Season #', s)
	processSeason(s)