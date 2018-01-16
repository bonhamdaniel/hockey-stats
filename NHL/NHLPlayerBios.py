import HockeyScrape
from unidecode import unidecode

# Gets NHL JSON Player file for each NHL Season in the db and adds all games to the db
def processPlayerBios(season):

	# Gets the json game file from the NHL api
	playerFile = HockeyScrape.getPlayers('NHL', season, 0)

	# Retrieves relevant data from the JSON game file
	players = []
	teams = playerFile['teams']
	for r in teams:
		try:
			for p in r['roster']['roster']:
				players.append(p['person'])
		except Exception as e:
			print(p)
			print(e)

	# Gets connection to specified database
	connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

	# Gets all valid player_ID's from the db
	cursor.execute('SELECT player_id FROM nhl_player_bio WHERE season_id = (%s)', (str(season), ))
	added = cursor.fetchall()
	for a in range(0, len(added)):
		added[a] = added[a][0]

	# Adds each player to the database
	for pl in players:

		if int(pl['id']) not in added:
			print('Adding player #', pl['id'], season)
			try:
				if 'weight' not in pl:
					pl['weight'] = 0.0
				if 'height' not in pl:
					height = 0.0
				else:
					height = pl['height'].replace(' ', '')
					height = height.replace('\\', '')
					height = height.replace('\"', '')
					height = height.replace("\'", ".")
				cursor.execute('INSERT INTO nhl_player_bio (player_id, season_id, height, weight, active, rookie, roster_status, position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (pl['id'], str(season), height, pl['weight'], pl['active'], pl['rookie'], pl['rosterStatus'], pl['primaryPosition']['abbreviation']))
				added.append(int(pl['id']))
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
	# Calls processPlayers() to add all NHL players to the db
	processPlayerBios(s[0])