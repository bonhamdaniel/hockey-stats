import HockeyScrape
import nhldb
import GameFeed
import sys

def processPXP(gameID):
	# Gets connection to specified database
	connection, cursor = HockeyScrape.getConnection('postgres', 'Hockey')

	# Gets JSON version of the GameFeed from utility function
	gameFile = HockeyScrape.getPXP('NHL', gameID)

	try:
		if (gameFile is not None) and ("Final" in gameFile["gameData"]["status"]["detailedState"]):
			# Adds an entry for each player who dressed to the nhl_player_dressed relation
			added = HockeyScrape.getDBPlayers('NHL', cursor)
			dressed = gameFile['gameData']['players']
			for d in dressed:
				d = dressed[d]
				if int(d['id']) not in added:
					HockeyScrape.addNHLPlayer(d, cursor)
				if 'primaryNumber' not in d:
					d['primaryNumber'] = -1
				if 'currentAge' not in d:
					d['currentAge'] = -1
				if 'alternateCaptain' not in d:
					d['alternateCaptain'] = False
				if 'captain' not in d:
					d['captain'] = False
				if ('ID' + str(d['id'])) in gameFile['liveData']['boxscore']['teams']['away']['players']:
					d['currentTeam'] = {"id": gameFile['liveData']['boxscore']['teams']['away']['team']['id']}
				elif ('ID' + str(d['id'])) in gameFile['liveData']['boxscore']['teams']['home']['players']:
					d['currentTeam'] = {"id": gameFile['liveData']['boxscore']['teams']['home']['team']['id']}
				cursor.execute('INSERT INTO nhl_player_dressed (player_id, game_id, num, age, assistant, captain, rookie, team, position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (d['id'], str(gameID), d['primaryNumber'], str(d['currentAge']), d['alternateCaptain'], d['captain'], d['rookie'], str(d['currentTeam']['id']), d['primaryPosition']['abbreviation']))
			
			# gets all game events
			events = gameFile["liveData"]["plays"]["allPlays"]

			# Loops through events, identifying each and writing to appropriate db tables
			for event in range(0, len(events)):
				eventType = events[event]['result']['event']
				if eventType in "Faceoff":
					team, winner, loser, period, time, awayGoals, homeGoals, xCoord, yCoord = GameFeed.getFaceoff(events, event)
					time = time.split(':')[0] + '.' + time.split(':')[1]
					#print('Faceoff', str(winner), str(loser), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
					fosql = 'INSERT INTO nhl_faceoff (game_id, event_id, team_id, winner, loser, period, time, away_goals, home_goals, x, y) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
					foparams = (str(gameID), str(events[event]['about']['eventIdx']), str(team), str(winner), str(loser), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
					cursor.execute(fosql, foparams)
				elif eventType in "Hit":	
					team, hitter, hittee, period, time, awayGoals, homeGoals, xCoord, yCoord = GameFeed.getHit(events, event)		
					time = time.split(':')[0] + '.' + time.split(':')[1]
					hitsql = 'INSERT INTO nhl_hit (game_id, event_id, team_id, hitter, hittee, period, time, away_goals, home_goals, x, y) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
					hitparams = (str(gameID), str(events[event]['about']['eventIdx']), str(team), str(hitter), str(hittee), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
					cursor.execute(hitsql, hitparams)
					#print('Hit', str(hitter), str(hittee), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
				elif eventType in "Giveaway":
					team, culprit, period, time, awayGoals, homeGoals, xCoord, yCoord = GameFeed.getGiveaway(events, event)
					time = time.split(':')[0] + '.' + time.split(':')[1]
					gasql = 'INSERT INTO nhl_giveaway (game_id, event_id, team_id, culprit, period, time, away_goals, home_goals, x, y) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
					gaparams = (str(gameID), str(events[event]['about']['eventIdx']), str(team), str(culprit), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
					cursor.execute(gasql, gaparams)
					#print('Giveaway', str(culprit), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
				elif eventType in "Shot":
					team, shooter, goalie, shot, period, time, awayGoals, homeGoals, xCoord, yCoord = GameFeed.getShot(events, event)
					time = time.split(':')[0] + '.' + time.split(':')[1]
					if "SHOOTOUT" in events[event]["about"]["periodType"]:
						result = 'save'
						glsql = 'INSERT INTO nhl_shootout (game_id, event_id, team_id, shooter, goalie, result, shot, x, y) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
						glparams = (str(gameID), str(events[event]['about']['eventIdx']), str(team), str(shooter), str(goalie), str(result), shot, str(xCoord), str(yCoord))
						cursor.execute(glsql, glparams)
					else:
						shsql = 'INSERT INTO nhl_shot (game_id, event_id, team_id, shooter, goalie, shot, period, time, away_goals, home_goals, x, y) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
						shparams = (str(gameID), str(events[event]['about']['eventIdx']), str(team), str(shooter), str(goalie), shot, str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
						cursor.execute(shsql, shparams)
					#print('Shot', str(shooter), str(goalie), shot, str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
				elif eventType in "Blocked Shot":
					team, blocker, shooter, period, time, awayGoals, homeGoals, xCoord, yCoord = GameFeed.getBlock(events, event)			
					time = time.split(':')[0] + '.' + time.split(':')[1]
					blsql = 'INSERT INTO nhl_block (game_id, event_id, team_id, blocker, shooter, period, time, away_goals, home_goals, x, y) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
					blparams = (str(gameID), str(events[event]['about']['eventIdx']), str(team), str(blocker), str(shooter), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
					cursor.execute(blsql, blparams)
					#print('Block', str(blocker), str(shooter), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
				elif eventType in "Missed Shot":
					team, culprit, period, time, awayGoals, homeGoals, xCoord, yCoord = GameFeed.getMiss(events, event)
					time = time.split(':')[0] + '.' + time.split(':')[1]
					if "SHOOTOUT" in events[event]["about"]["periodType"]:
						goalie = 0
						result = 'miss'
						shot = 'n/a'
						glsql = 'INSERT INTO nhl_shootout (game_id, event_id, team_id, shooter, goalie, result, shot, x, y) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
						glparams = (str(gameID), str(events[event]['about']['eventIdx']), str(team), str(culprit), str(goalie), str(result), shot, str(xCoord), str(yCoord))
						cursor.execute(glsql, glparams)
					else:		
						mssql = 'INSERT INTO nhl_miss (game_id, event_id, team_id, culprit, period, time, away_goals, home_goals, x, y) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
						msparams = (str(gameID), str(events[event]['about']['eventIdx']), str(team), str(culprit), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
						cursor.execute(mssql, msparams)
					#print('Missed Shot', str(culprit), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
				elif eventType in "Takeaway":
					team, taker, period, time, awayGoals, homeGoals, xCoord, yCoord = GameFeed.getTakeaway(events, event)
					time = time.split(':')[0] + '.' + time.split(':')[1]
					tasql = 'INSERT INTO nhl_takeaway (game_id, event_id, team_id, taker, period, time, away_goals, home_goals, x, y) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
					taparams = (str(gameID), str(events[event]['about']['eventIdx']), str(team), str(taker), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
					cursor.execute(tasql, taparams)
					#print('Takeaway', str(taker), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
				elif eventType in "Penalty":
					team, taker, drawer, penalty, minutes, period, time, awayGoals, homeGoals, xCoord, yCoord = GameFeed.getPenalty(events, event)
					time = time.split(':')[0] + '.' + time.split(':')[1]
					#print('Penalty', str(drawer), str(taker), penalty, str(minutes), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
					pensql = 'INSERT INTO nhl_penalty (game_id, event_id, team_id, taker, drawer, penalty, minutes, period, time, away_goals, home_goals, x, y) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
					penparams = (str(gameID), str(events[event]['about']['eventIdx']), str(team), str(taker), str(drawer), penalty, str(minutes), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
					cursor.execute(pensql, penparams)
				elif eventType in "Goal":
					team, scorer, primary, secondary, goalie, shot, situation, gwg, en, period, time, awayGoals, homeGoals, xCoord, yCoord = GameFeed.getGoal(events, event)
					time = time.split(':')[0] + '.' + time.split(':')[1]
					if "SHOOTOUT" in events[event]["about"]["periodType"]:
						result = 'goal'
						glsql = 'INSERT INTO nhl_shootout (game_id, event_id, team_id, shooter, goalie, result, shot, x, y) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
						glparams = (str(gameID), str(events[event]['about']['eventIdx']), str(team), str(scorer), str(goalie), str(result), shot, str(xCoord), str(yCoord))
						cursor.execute(glsql, glparams)
					else:
						cursor.execute('INSERT INTO nhl_goal (game_id, event_id, team_id, scorer, goalie, period, time, away_goals, home_goals, x, y, shot, a1, a2, situation, gwg, en) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (str(gameID), str(events[event]['about']['eventIdx']), str(team), str(scorer), str(goalie), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord), shot, str(primary), str(secondary), situation, bool(gwg), bool(en)))
				
						shsql = 'INSERT INTO nhl_shot (game_id, event_id, team_id, shooter, goalie, shot, period, time, away_goals, home_goals, x, y) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
						shparams = (str(gameID), str(events[event]['about']['eventIdx']), str(team), str(scorer), str(goalie), shot, str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
						cursor.execute(shsql, shparams)
					#print('Goal', str(scorer), str(primary), str(secondary), str(goalie), shot, situation, gwg, en, str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
				else: # Should catch an unexpected events
					current = eventType
					if current not in "Game Scheduled" and current not in "Period Ready" and current not in "Period Start" and current not in "Stoppage" and current not in "Period End" and current not in "Period Official" and current not in "Game End" and current not in "Official Challenge" and current not in "Game Official" and current not in "Shootout Complete" and current not in "Early Intermission Start" and current not in "Early Intermission End":
						print(current)

			# Gets Team Boxscore JSON, summarizes team totals, and writes team summaries to db
			boxscore = gameFile["liveData"]["boxscore"]
			aTeam, aGoals, aPIM, aShots, aPPG, aPPOPP, aBlocks, aTA, aGA, aHits, hTeam, hGoals, hPIM, hShots, hPPG, hPPOPP, hBlocks, hTA, hGA, hHits = GameFeed.getTeamSummary(boxscore)
			
			# Gets away team players that played in game
			aTeam = 'away'
			awayTeam, awayPlayers, apKeys = GameFeed.getTeamPlayers(gameFile, aTeam)

			# Gets away team players that played in game
			hTeam = 'home'
			homeTeam, homePlayers, hpKeys = GameFeed.getTeamPlayers(gameFile, hTeam)

			# Gets rinkside for each team, each period that they play
			periods = gameFile['liveData']['linescore']['periods']
			for per in periods:
				if 'rinkSide' in per['away']:
					aRinkSide = per['away']['rinkSide']
				else:
					aRinkSide = ''
				if 'rinkSide' in per['home']:
					hRinkSide = per['home']['rinkSide']
				else:
					hRinkSide = ''
				cursor.execute('INSERT INTO nhl_rink_side (game_id, period, team_id, rink_side) VALUES (%s, %s, %s, %s)', (str(gameID), per['num'], str(awayTeam), aRinkSide))
				cursor.execute('INSERT INTO nhl_rink_side (game_id, period, team_id, rink_side) VALUES (%s, %s, %s, %s)', (str(gameID), per['num'], str(homeTeam), hRinkSide))

			tsql = 'INSERT INTO nhl_team_summary (game_id, away_team, home_team, away_goals, home_goals, away_pim, home_pim, away_shots, home_shots, away_ppg, home_ppg, away_ppo, home_ppo, away_blocks, home_blocks, away_ta, home_ta, away_ga, home_ga, away_hits, home_hits) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
			tparams = (str(gameID), str(awayTeam), str(homeTeam), str(aGoals), str(hGoals), str(aPIM), str(hPIM), str(aShots), str(hShots), str(int(aPPG)), str(int(hPPG)), str(int(aPPOPP)), str(int(hPPOPP)), str(aBlocks), str(hBlocks), str(aTA), str(hTA), str(aGA), str(hGA), str(aHits), str(hHits))
			cursor.execute(tsql, tparams)

			# Loops through away team players, compiles individual game summaries, and writes them to the db
			for player in range(0, len(awayPlayers)):	
				playerID = awayPlayers[apKeys[player]]["person"]["id"]
				location = 'Away'
				position = awayPlayers[apKeys[player]]["position"]["abbreviation"].strip()
				if position not in 'G' and len(awayPlayers[apKeys[player]]["stats"]) > 0:
					no, toi, assists, goals, shots, hits, ppg, ppa, pim, fow, fot, ta, ga, shg, sha, blocks, plusMinus, EVTOI, PPTOI, SHTOI = GameFeed.getSkaterSummary(awayPlayers, apKeys, player)
					apsql = 'INSERT INTO nhl_skater_summary (game_id, location, team, player_id, num, position, toi, assists, goals, shots, hits, ppg, ppa, pim, fow, fot, ta, ga, shg, sha, blocks, plus_minus, ev_toi, pp_toi, sh_toi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
					apparams = (str(gameID), str(location), str(awayTeam), str(playerID), str(no), position, str(toi), str(assists), str(goals), str(shots), str(hits), str(ppg), str(ppa), str(pim), str(fow), str(fot), str(ta), str(ga), str(shg), str(sha), str(blocks), str(plusMinus), str(EVTOI), str(PPTOI), str(SHTOI))
					cursor.execute(apsql, apparams)
					#cursor.commit()
				elif position in 'G' and len(awayPlayers[apKeys[player]]["stats"]) > 0:
					no, toi, assists, goals, pim, shots, saves, ppsv, shsv, evsv, shsa, evsa, ppsa, decision, svpct, evsvpct = GameFeed.getGoalieSummary(awayPlayers, apKeys, player)
					agsql = 'INSERT INTO nhl_goalie_summary (game_id, location, team_id, player_id, num, toi, assists, goals, pim, shots, saves, ppsv, shsv, evsv, shsa, evsa, ppsa, decision, svpct, ev_svpct) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
					agparams = (str(gameID), location, str(awayTeam), str(playerID), no, str(toi), str(assists), str(goals), str(pim), str(shots), str(saves), str(ppsv), str(shsv), str(evsv), str(shsa), str(evsa), str(ppsa), decision, str(svpct), str(evsvpct))
					cursor.execute(agsql, agparams)
					#cursor.commit()
			del apKeys	

			for player in range(0, len(homePlayers)):	
				playerID = homePlayers[hpKeys[player]]["person"]["id"]
				location = 'Home'
				position = homePlayers[hpKeys[player]]["position"]["abbreviation"].strip()
				if position not in 'G' and len(homePlayers[hpKeys[player]]["stats"]) > 0:
					no, toi, assists, goals, shots, hits, ppg, ppa, pim, fow, fot, ta, ga, shg, sha, blocks, plusMinus, EVTOI, PPTOI, SHTOI = GameFeed.getSkaterSummary(homePlayers, hpKeys, player)
					apsql = 'INSERT INTO nhl_skater_summary (game_id, location, team, player_id, num, position, toi, assists, goals, shots, hits, ppg, ppa, pim, fow, fot, ta, ga, shg, sha, blocks, plus_minus, ev_toi, pp_toi, sh_toi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
					apparams = (str(gameID), str(location), str(homeTeam), str(playerID), str(no), position, str(toi), str(assists), str(goals), str(shots), str(hits), str(ppg), str(ppa), str(pim), str(fow), str(fot), str(ta), str(ga), str(shg), str(sha), str(blocks), str(plusMinus), str(EVTOI), str(PPTOI), str(SHTOI))
					cursor.execute(apsql, apparams)
				elif position in 'G' and len(homePlayers[hpKeys[player]]["stats"]) > 0:
					no, toi, assists, goals, pim, shots, saves, ppsv, shsv, evsv, shsa, evsa, ppsa, decision, svpct, evsvpct = GameFeed.getGoalieSummary(homePlayers, hpKeys, player)
					agsql = 'INSERT INTO nhl_goalie_summary (game_id, location, team_id, player_id, num, toi, assists, goals, pim, shots, saves, ppsv, shsv, evsv, shsa, evsa, ppsa, decision, svpct, ev_svpct) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
					agparams = (str(gameID), location, str(homeTeam), str(playerID), no, str(toi), str(assists), str(goals), str(pim), str(shots), str(saves), str(ppsv), str(shsv), str(evsv), str(shsa), str(evsa), str(ppsa), decision, str(svpct), str(evsvpct))
					cursor.execute(agsql, agparams)
			del hpKeys

			# Gets Head Coaches and writes to db
			if len(gameFile['liveData']['boxscore']['teams']['away']['coaches']) > 0:
				cursor.execute('INSERT INTO nhl_head_coach (game_id, away, home) VALUES (%s, %s, %s)', (str(gameID), gameFile['liveData']['boxscore']['teams']['away']['coaches'][0]['person']['fullName'], gameFile['liveData']['boxscore']['teams']['home']['coaches'][0]['person']['fullName']))

			# Gets Officials and writes to nhl db
			#if len(gameFile['liveData']['boxscore']['officials']):
			referees, linesmen = GameFeed.getOfficials(gameFile)
			if referees[0] > 0:
				cursor.execute('INSERT INTO nhl_officials (game_id, referee1_id, referee2_id, linesman1_id, linesman2_id) VALUES (%s, %s, %s, %s, %s)', (str(gameID), str(referees[0]), str(referees[1]), str(linesmen[0]), str(linesmen[1])))
			
			# Gets Three Star Selections and writes to nhldb
			firstStar, secondStar, thirdStar = GameFeed.getStars(gameFile)
			if firstStar > 0:
				ssql = 'INSERT INTO nhl_stars (game_id, first_star, second_star, third_star) VALUES (%s, %s, %s, %s)'
				sparams = (str(gameID), str(firstStar), str(secondStar), str(thirdStar))
				cursor.execute(ssql, sparams)


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

# Gets all valid game_id's from the db
cursor.execute('SELECT game_id FROM nhl_team_summary')
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
	processPXP(g)