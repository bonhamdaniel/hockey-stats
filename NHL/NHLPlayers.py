import HockeyScrape
from unidecode import unidecode

# Gets NHL JSON Player file for each NHL Season in the db and adds all games to the db
def processPlayers(season, added):

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

	# Adds each player to the database
	for pl in players:
		if int(pl['id']) not in added:
			print('Adding player #', pl['id'])
			try:
				if 'birthStateProvince' not in pl:
					pl['birthStateProvince'] = ''
				if 'shootsCatches' not in pl:
					pl['shootsCatches'] = ''
				if 'birthCity' not in pl:
					pl['birthCity'] = ''
				cursor.execute('INSERT INTO nhl_player (player_id, first_name, last_name, birthdate, shoots, player_name, town, province, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (pl['id'], unidecode(pl['firstName'].strip()), unidecode(pl['lastName'].strip()), pl['birthDate'], pl['shootsCatches'], unidecode(pl['lastName'].strip()) + '.' + unidecode(pl['firstName'].strip()), pl['birthCity'], pl['birthStateProvince'], pl['birthCountry']))
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

# Gets all valid player_ID's from the db
cursor.execute('SELECT player_id FROM nhl_player')
players = cursor.fetchall()
for p in range(0, len(players)):
	players[p] = players[p][0]

# Commits DB changes and closes the connection
connection.commit()
connection.close()

for s in seasons:
	print(s[0])
	# Calls processPlayers() to add all NHL players to the db
	processPlayers(s[0], players)