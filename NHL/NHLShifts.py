import HockeyScrape
import nhldb
import GameFeed
#import sys

def processShifts(gameID):
	# Gets connection to specified database
	connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

	# Gets JSON version of the Shifts file from the NHL api
	gameFile = HockeyScrape.getShifts('NHL', gameID)

	try:
		# Adds an entry for each player who dressed to the nhl_player_dressed relation
		shifts = gameFile['data']
		if len(shifts) > 0:
			for s in shifts:
				if s['eventNumber'] is None:
					s['eventNumber'] = -1
				if s['eventDescription'] is None:
					s['eventDescription'] = 'n/a'
				if s['eventDetails'] is None:
					s['eventDetails'] = 'n/a'
				if s['detailCode'] is None:
					s['detailCode'] = -1
				if s['duration'] is None:
					s['duration'] = '0:00'
				startTime = HockeyScrape.convertTime(s['startTime'])
				endTime = HockeyScrape.convertTime(s['endTime'])
				duration = HockeyScrape.convertTime(s['duration'])
				sql = 'INSERT INTO nhl_shift (game_id, shift_id, player_id, team_id, num, period, start_time, end_time, duration, code, event, details, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
				params = (s['gameId'], s['eventNumber'], s['playerId'], s['teamId'], s['shiftNumber'], s['period'], startTime, endTime, duration, s['detailCode'], s['eventDescription'], s['eventDetails'], s['typeCode'])
				cursor.execute(sql, params)

			connection.commit()
			connection.close()

	except Exception as e:
		print(sys.exc_info()[0])
		print(type(e))

# Gets connection to specified database
connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

# Gets all valid game_id's from the db
cursor.execute('SELECT game_id FROM nhl_game')
games = cursor.fetchall()
for g in range(0, len(games)):
	games[g] = games[g][0]

# Gets all valid game_id's from the db
cursor.execute('SELECT game_id FROM nhl_shift')
added = cursor.fetchall()
for a in range(0, len(added)):
	added[a] = added[a][0]

games = list(set(games) - set(added))

# Commits DB changes and closes the connection
connection.commit()
connection.close()

for g in games:
	#if g[0] not in added:
	print("Processing game #" + str(g))
	processShifts(g)