import HockeyScrape
from unidecode import unidecode

# Processes each Season/Team pair in the db, adding any missing players
def processPlayers(season, team, added):
	# Gets the json roster file for the season/team pair
	rosterFile = HockeyScrape.getPlayers('OHL', season, team)

	# Retrieves player bio data from the JSON roster file
	players = rosterFile['SiteKit']['Roster']

	# Gets connection to specified database
	connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

	# Adds each missing player to the database
	for p in players:
		try:
			# Checks if player already present in the db
			if int(p['id']) not in added:
				# Checks for, and remedies, any missing birthdates
				if p['rawbirthdate'] == "":
					p['rawbirthdate'] = '1900-01-01 00:00:00'

				# Checks for and remedies any missing or malformed height values
				if p['height'] == "":
					p['height'] = 0.0
				else:
					p['height'] = p['height'].replace('\'', '.')
					p['height'] = p['height'].replace('-', '.')
					p['height'] = p['height'][0:4]

				# Checks for and remedies any missing weight values
				if p['weight'] == "":
					p['weight'] = 0

				# Adds player to the db
				cursor.execute('INSERT INTO ohl_player (player_id, first_name, last_name, player_name, shoots, town, province, country, height, weight, birthdate, position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (p['id'], unidecode(p['first_name'].strip()), unidecode(p['last_name'].strip()), unidecode(p['last_name'].strip()) + '.' + unidecode(p['first_name'].strip()), p['shoots'], p['hometown'], p['homeprov'], p['homecntry'], p['height'], p['weight'], p['rawbirthdate'], p['position']))
				added.append(int(p['id']))
		except Exception as e:
			print(e)

	# Commits DB canges and closes the connection
	connection.commit()
	connection.close()

# Gets connection to specified database
connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

# Gets dict of all season/team pairs in the db
cursor.execute('SELECT season_id, team_id FROM ohl_team')
results = cursor.fetchall()

# Gets dict of all players already preent in the db
cursor.execute('SELECT player_id FROM ohl_player')
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