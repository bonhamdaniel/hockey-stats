import HockeyScrape
import nhldb
import GameFeed
#import sys

def processFOT(gameID):
	# Gets connection to specified database
	connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

	# Gets JSON version of the GameFeed from utility function
	gameFile = HockeyScrape.getPXP('NHL', gameID)

	try:
		if (gameFile is not None) and ("Final" in gameFile["gameData"]["status"]["detailedState"]):
			# Gets away team players that played in game
			aTeam = 'away'
			awayTeam, awayPlayers, apKeys = GameFeed.getTeamPlayers(gameFile, aTeam)

			# Gets away team players that played in game
			hTeam = 'home'
			homeTeam, homePlayers, hpKeys = GameFeed.getTeamPlayers(gameFile, hTeam)

			# Loops through away team players, compiles individual game summaries, and writes them to the db
			for player in range(0, len(awayPlayers)):	
				playerID = awayPlayers[apKeys[player]]["person"]["id"]
				position = awayPlayers[apKeys[player]]["position"]["abbreviation"].strip()
				if position not in 'G' and len(awayPlayers[apKeys[player]]["stats"]) > 0:
					if "faceoffTaken" in awayPlayers[apKeys[player]]["stats"]["skaterStats"]:
						fot = awayPlayers[apKeys[player]]["stats"]["skaterStats"]["faceoffTaken"]
					else:
						fot = 0
					apsql = 'UPDATE nhl_skater_summary SET fot = %s WHERE player_id = %s'
					apparams = (str(fot), str(playerID))
					cursor.execute(apsql, apparams)
			del apKeys	

			for player in range(0, len(homePlayers)):	
				playerID = homePlayers[hpKeys[player]]["person"]["id"]
				position = homePlayers[hpKeys[player]]["position"]["abbreviation"].strip()
				if position not in 'G' and len(homePlayers[hpKeys[player]]["stats"]) > 0:
					if "faceoffTaken" in homePlayers[hpKeys[player]]["stats"]["skaterStats"]:
						fot = homePlayers[hpKeys[player]]["stats"]["skaterStats"]["faceoffTaken"]
					else:
						fot = 0
					apsql = 'UPDATE nhl_skater_summary SET fot = %s WHERE player_id = %s'
					apparams = (str(fot), str(playerID))
					cursor.execute(apsql, apparams)
			del hpKeys

			# Commits all transactions to the db and closes the connection
			connection.commit()
			connection.close()

		else:
			print("No game #", gameID)

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

# Commits DB changes and closes the connection
connection.commit()
connection.close()

for g in games:
	#if g[0] not in added:
	print("Processing game #" + str(g))
	processFOT(g)