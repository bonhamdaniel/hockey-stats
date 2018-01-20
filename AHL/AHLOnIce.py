import sys
import HockeyScrape
from unidecode import unidecode

# Procsses the JSON play-by-play file for the specified game, adding each event to its appropriate db relation
def processOnIce(gameID):
	try:
		# Gets the json play-by-play file
		pxpFile = HockeyScrape.getPXP('AHL', gameID)

		# Gets connection to specified database
		connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

		# Retrieves relevant data from the JSON play-by-play file
		events = pxpFile

		# Gets players from db
		cursor.execute('SELECT player_id FROM ahl_player')
		players = cursor.fetchall()
		for p in range(len(players)):
			players[p] = players[p][0]

		# Will hold players active in current game
		current = []

		# Gets players active in current game
		homeStats = events['homeTeam']
		visitingStats = events['visitingTeam']
		for hg in homeStats['goalies']:
			current.append(hg['info']['id'])
		for vg in visitingStats['goalies']:
			current.append(vg['info']['id'])
		for hp in homeStats['skaters']:
			current.append(hp['info']['id'])
		for vp in visitingStats['skaters']:
			current.append(vp['info']['id'])

		# Adds any players not already in the db
		for c in current:
			if int(c) not in players:
				# Gets JSON player bio from
				cp = HockeyScrape.getPlayer('AHL', c)
				p = cp['info']

				if len(p) > 2:
					# Checks for, and remedies, any missing birthdates
					if p['birthDate'] == "":
						p['birthDate'] = '1900-01-01 00:00:00'

					# Checks for and remedies any missing or malformed height values
					if p['height'] == "":
						p['height'] = 0.0
					else:
						p['height'] = p['height'].replace('\'', '.')
						p['height'] = p['height'].replace('-', '.')
						p['height'] = p['height'][0:4]

					# Checks for and remedies any missing weight values
					if p['weight'] == "" or '-' in p['weight']:
						p['weight'] = 0

					# Changes 'shoots' attribute to 'catches' for goalies
					if p['position'] == "G":
						p['shoots'] = p['catches']

					# Adds player to the db
					cursor.execute('INSERT INTO ahl_player (player_id, first_name, last_name, player_name, shoots, birthplace, height, weight, birthdate, position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (c, unidecode(p['firstName'].strip()), unidecode(p['lastName'].strip()), unidecode(p['lastName'].strip()) + '.' + unidecode(p['firstName'].strip()), p['shoots'], p['birthPlace'], p['height'], p['weight'], p['birthDate'], p['position']))
		
		# Process Goals and Assists
		periods = events['periods']
		for p in periods:
			period = p['info']['id']
			goals = p['goals']
			
			for g in goals:
				time = HockeyScrape.getGameTime(period, g['time'])
				plus = []
				for pen in range(0, len(g['plus_players'])):
					if g['plus_players'][pen]['id'] not in plus:
						plus.append(g['plus_players'][pen]['id'])
						cursor.execute('INSERT INTO ahl_goal_for (game_id, time, player_id) VALUES (%s, %s, %s)', (str(gameID), time, str(g['plus_players'][pen]['id'])))

				for m in range(0, len(g['minus_players'])):
					cursor.execute('INSERT INTO ahl_goal_against (game_id, time, player_id) VALUES (%s, %s, %s)', (str(gameID), time, str(g['minus_players'][m]['id'])))				

		# Closes db connection
		connection.commit()
		connection.close()

	except Exception as e:
		e_type, e_object, e_tb = sys.exc_info
		print(e_tb)
		input("Press Enter to continue...")

# Gets connection to specified database
connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

# Gets dict of all games already in the db
cursor.execute('SELECT game_id FROM ahl_game')
games = cursor.fetchall()
for g in range(len(games)):
	games[g] = games[g][0]

# Gets dict of all games already in the db
cursor.execute('SELECT game_id FROM ahl_goal_for')
added = cursor.fetchall()
for a in range(len(added)):
	added[a] = added[a][0]

# Closes db connection
connection.commit()
connection.close()

games = list(set(games) - set(added))

# Loops through each specified season, processing game results
for g in games:
	print('Processing Game #', g)
	processOnIce(g)