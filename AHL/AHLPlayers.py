import HockeyScrape
from unidecode import unidecode

# Processes each Season/Team pair in the db, adding any missing players
def processPlayers(season, team, added):
	# Gets the json roster file for the season/team pair
	rosterFile = HockeyScrape.getPlayers('AHL', season, team)

	# Retrieves player bio data from the JSON roster file
	players = rosterFile['roster'][0]['sections']
	forwards = players[0]['data']
	defence = players[1]['data']
	goalies = players[2]['data']
	players = forwards+defence+goalies
	#print(players)

	# Gets connection to specified database
	connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

	# Adds each missing player to the database
	for p in players:
		try:
			# Checks if player already present in the db
			if int(p['row']['player_id']) not in added:
				print(p['row']['name'])
				# Checks for, and remedies, any missing birthdates
				if p['row']['birthdate'] == "":
					p['row']['birthdate'] = '1900-01-01 00:00:00'

				# Checks for and remedies any missing or malformed height values
				if 'height_hyphenated' not in p['row']:
					p['row']['height_hyphenated'] = p['row']['h']
				
				if p['row']['height_hyphenated'] == "":
					p['row']['height_hyphenated'] = 0.0
				else:
					p['row']['height_hyphenated'] = p['row']['height_hyphenated'].replace('\'', '.')
					p['row']['height_hyphenated'] = p['row']['height_hyphenated'].replace('-', '.')
					#p['height_hyphenated'] = p['height'][0:4]

				# Checks for and remedies any missing or erroneous weight values
				if '-' in p['row']['w']:
					p['row']['height_hyphenated'] = p['row']['w']
					p['row']['w'] = 0
				elif p['row']['w'] == "":
					p['row']['w'] = 0

				# Changes 'shoots' attribute to 'catches' for goalies
				if p['row']['position'] == "G":
					p['row']['shoots'] = p['row']['catches']

				# Formats name
				if "  " in p['row']['name']:
					firstName, lastName = (p['row']['name']).split("  ")
				elif len((p['row']['name']).split(" ")) > 3:
					firstName, x, y, lastName = (p['row']['name']).split(" ")
					lastName = x + " " + y + " " + lastName
				elif len((p['row']['name']).split(" ")) > 2:
					firstName, x, lastName = (p['row']['name']).split(" ")
					lastName = x + " " + lastName
				else:
					firstName, lastName = (p['row']['name']).split(" ")

				# Adds player to the db
				cursor.execute('INSERT INTO ahl_player (player_id, first_name, last_name, player_name, shoots, birthplace, height, weight, birthdate, position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (p['row']['player_id'], unidecode(firstName.strip()), unidecode(lastName.strip()), unidecode(lastName.strip()) + '.' + unidecode(firstName.strip()), p['row']['shoots'], p['row']['birthplace'], p['row']['height_hyphenated'], p['row']['w'], p['row']['birthdate'], p['row']['position']))
				added.append(int(p['row']['player_id']))
		except Exception as e:
			print(e)

	# Commits DB canges and closes the connection
	connection.commit()
	connection.close()

# Gets connection to specified database
connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

# Gets dict of all season/team pairs in the db
cursor.execute('SELECT season_id, team_id FROM ahl_team')
results = cursor.fetchall()

# Gets dict of all players already preent in the db
cursor.execute('SELECT player_id FROM ahl_player')
added = cursor.fetchall()
for a in range(0, len(added)):
	added[a] = added[a][0]

# Closes the db connection
connection.commit()
connection.close()

# Processes each Season/Team pair, adding any players missing from db
for r in results:
	print('Processing Season #', r[0], 'Team #', r[1])
	processPlayers(r[0], r[1], added)