#nhldb.py
import pyodbc
import os
from unidecode import unidecode

def getConnection(dbName):
	dbFile = 'NHL.accdb'
	if dbFile.split('.')[1] in 'accdb' or dbFile.split[1] in 'mdb':
		driver = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
	else:
		driver = ''
	connectionString = (driver + 'DBQ=C:/pythonprograms/nhl/' + dbFile + ';')
	connection = pyodbc.connect(connectionString)
	connection.setencoding(encoding='utf-8')
	cursor = connection.cursor()
	return connection, cursor

def writeGameInfo(cursor, gameID, season, seasonType, date, awayTeam, homeTeam, awaySide, homeSide, ot, so):
	gamesql = """INSERT INTO [Game] ([GameID], [SeasonID], [SeasonType], [GameDate], [AwayTeam], [HomeTeam], [AwaySide], [HomeSide], [OT], [SO]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
	gameparams = (str(gameID), season, seasonType, date, str(awayTeam), str(homeTeam), awaySide, homeSide, ot, so)
	cursor.execute(gamesql, gameparams)

def writePlayers(cursor, players, keys):
	for player in range(0, len(players)):	
		playerID = players[keys[player]]["id"]

		sql = """SELECT * FROM [Player] WHERE [PlayerID] = ?"""
		params = (str(playerID))
		cursor.execute(sql, params)
		results = cursor.fetchall()

		if len(results) == 0:
			firstName = unidecode(players[keys[player]]["firstName"].strip())
			lastName = unidecode(players[keys[player]]["lastName"].strip())
			playerName = lastName + '.' + firstName
			birthdate = players[keys[player]]["birthDate"].strip()
			country = players[keys[player]]["birthCountry"].strip()
			if "height" in players[keys[player]]:
				height = players[keys[player]]["height"].strip()
			else:
				height = "0"
			if "weight" in players[keys[player]]:
				weight = players[keys[player]]["weight"]
			else:
				weight = "0"
			if "shootsCatches" in players[keys[player]]:
				hand = players[keys[player]]["shootsCatches"].strip()
			else:
				hand = 'n/a'
			position = players[keys[player]]["primaryPosition"]["code"].strip()

			psql = """INSERT INTO [Player] ([PlayerID], [FirstName], [LastName], [PlayerName], [Birthdate], [Country], [Height], [Weight], [Hand], [Position]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
			pparams = (str(playerID), firstName, lastName, playerName, str(birthdate), country, height, str(weight), hand, position)
			cursor.execute(psql, pparams)

def writeFaceoff(cursor, gameID, team, winner, loser, period, time, awayGoals, homeGoals, xCoord, yCoord):
	fosql = """INSERT INTO [Faceoff] ([GameID], [TeamID], [Winner], [Loser], [Period], [Time], [AwayGoals], [HomeGoals], [XCoord], [YCoord]) VALUES (?, ?,?,?,?,?,?,?,?,?)"""
	foparams = (str(gameID), str(team), str(winner), str(loser), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
	cursor.execute(fosql, foparams)

def writeHit(cursor, gameID, team, hitter, hittee, period, time, awayGoals, homeGoals, xCoord, yCoord):
	hitsql = """INSERT INTO [Hit] ([GameID], [TeamID], [Hitter], [Hittee], [Period], [Time], [AwayGoals], [HomeGoals], [XCoord], [YCoord]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
	hitparams = (str(gameID), str(team), str(hitter), str(hittee), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
	cursor.execute(hitsql, hitparams)

def writeGiveaway(cursor, gameID, team, culprit, period, time, awayGoals, homeGoals, xCoord, yCoord):
	gasql = """INSERT INTO [Giveaway] ([GameID], [TeamID], [Culprit], [Period], [Time], [AwayGoals], [HomeGoals], [XCoord], [YCoord]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
	gaparams = (str(gameID), str(team), str(culprit), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
	cursor.execute(gasql, gaparams)

def writeShot(cursor, gameID, team, shooter, goalie, shot, period, time, awayGoals, homeGoals, xCoord, yCoord):
	shsql = """INSERT INTO [Shot] ([GameID], [TeamID], [Shooter], [Goalie], [Shot], [Period], [Time], [AwayGoals], [HomeGoals], [XCoord], [YCoord]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
	shparams = (str(gameID), str(team), str(shooter), str(goalie), shot, str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
	cursor.execute(shsql, shparams)

def writeShootout(cursor, gameID, team, shooter, goalie, result, shot, xCoord, yCoord):
	glsql = """INSERT INTO [Shootout] ([GameID], [TeamID], [Shooter], [Goalie], [Result], [Shot], [XCoord], [YCoord]) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
	glparams = (str(gameID), str(team), str(shooter), str(goalie), str(result), shot, str(xCoord), str(yCoord))
	cursor.execute(glsql, glparams)

def writeBlock(cursor, gameID, team, blocker, shooter, period, time, awayGoals, homeGoals, xCoord, yCoord):
	blsql = """INSERT INTO [Block] ([GameID], [TeamID], [Blocker], [Shooter], [Period], [Time], [AwayGoals], [HomeGoals], [XCoord], [YCoord]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
	blparams = (str(gameID), str(team), str(blocker), str(shooter), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
	cursor.execute(blsql, blparams)

def writeMiss(cursor, gameID, team, culprit, period, time, awayGoals, homeGoals, xCoord, yCoord):
	mssql = """INSERT INTO [MissedShot] ([GameID], [TeamID], [Culprit], [Period], [Time], [AwayGoals], [HomeGoals], [XCoord], [YCoord]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
	msparams = (str(gameID), str(team), str(culprit), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
	cursor.execute(mssql, msparams)

def writeTakeaway(cursor, gameID, team, taker, period, time, awayGoals, homeGoals, xCoord, yCoord):
	tasql = """INSERT INTO [Takeaway] ([GameID], [TeamID], [Taker], [Period], [Time], [AwayGoals], [HomeGoals], [XCoord], [YCoord]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
	taparams = (str(gameID), str(team), str(taker), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
	cursor.execute(tasql, taparams)

def writePenalty(cursor, gameID, team, taker, drawer, penalty, minutes, period, time, awayGoals, homeGoals, xCoord, yCoord):
	pensql = """INSERT INTO [Penalty] ([GameID], [TeamID], [Taker], [Drawer], [Penalty], [Minutes], [Period], [Time], [AwayGoals], [HomeGoals], [XCoord], [YCoord]) VALUES (?, ?,?,?,?,?,?,?,?,?,?,?)"""
	penparams = (str(gameID), str(team), str(taker), str(drawer), penalty, str(minutes), str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
	cursor.execute(pensql, penparams)

def writeGoal(cursor, gameID, team, scorer, primary, secondary, goalie, shot, situation, gwg, en, period, time, awayGoals, homeGoals, xCoord, yCoord):
	glsql = """INSERT INTO [Goal] ([GameID], [TeamID], [Scorer], [Primary], [Secondary], [Goalie], [Shot], [Situation], [GWG], [EN], [Period], [Time], [AwayGoals], [HomeGoals], [XCoord], [YCoord]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
	glparams = (str(gameID), str(team), str(scorer), str(primary), str(secondary), str(goalie), shot, situation, gwg, en, str(period), time, str(awayGoals), str(homeGoals), str(xCoord), str(yCoord))
	cursor.execute(glsql, glparams)

def writeTeamSummary(cursor, gameID, aTeam, aGoals, aPIM, aShots, aPPG, aPPOPP, aBlocks, aTA, aGA, aHits, hTeam, hGoals, hPIM, hShots, hPPG, hPPOPP, hBlocks, hTA, hGA, hHits):
	tsql = """INSERT INTO [TeamSummary] ([GameID], [AwayTeam], [HomeTeam], [AwayGoals], [HomeGoals], [AwayPIM], [HomePIM], [AwayShots], [HomeShots], [AwayPPG], [HomePPG], [AwayPPOPP], [HomePPOPP], [AwayBlocks], [HomeBlocks], [AwayTA], [HomeTA], [AwayGA], [HomeGA], [AwayHits], [HomeHits]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
	tparams = (str(gameID), str(aTeam), str(hTeam), str(aGoals), str(hGoals), str(aPIM), str(hPIM), str(aShots), str(hShots), str(aPPG), str(hPPG), str(aPPOPP), str(hPPOPP), str(aBlocks), str(hBlocks), str(aTA), str(hTA), str(aGA), str(hGA), str(aHits), str(hHits))
	cursor.execute(tsql, tparams)

def writePlayerSummary(cursor, gameID, location, team, playerID, no, position, toi, assists, goals, shots, hits, ppg, ppa, pim, fow, fot, ta, ga, shg, sha, blocks, plusMinus, EVTOI, PPTOI, SHTOI):
	apsql = """INSERT INTO [PlayerSummary] ([GameID], [Location], [Team], [PlayerID], [JerseyNo], [Position], [TOI], [Assists], [Goals], [Shots], [Hits], [PPG], [PPA], [PIM], [FOW], [FOT], [TA], [GA], [SHG], [SHA], [Blocks], [PlusMinus], [EVTOI], [PPTOI], [SHTOI]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
	apparams = (str(gameID), str(location), str(team), str(playerID), str(no), position, str(toi), str(assists), str(goals), str(shots), str(hits), str(ppg), str(ppa), str(pim), str(fow), str(fot), str(ta), str(ga), str(shg), str(sha), str(blocks), str(plusMinus), str(EVTOI), str(PPTOI), str(SHTOI))
	cursor.execute(apsql, apparams)

def writeGoalieSummary(cursor, gameID, location, team, playerID, no, toi, assists, goals, pim, shots, saves, ppsv, shsv, evsv, shsa, evsa, ppsa, decision, svpct, evsvpct):
	agsql = """INSERT INTO [GoalieSummary] ([GameID], [Location], [Team], [PlayerID], [JerseyNo], [TOI], [Assists], [Goals], [PIM], [Shots], [Saves], [PPSV], [SHSV], [EVSV], [SHSA], [EVSA], [PPSA], [Decision], [SVPCT], [EVSVPCT]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
	agparams = (str(gameID), location, str(team), str(playerID), no, str(toi), str(assists), str(goals), str(pim), str(shots), str(saves), str(ppsv), str(shsv), str(evsv), str(shsa), str(evsa), str(ppsa), decision, str(svpct), str(evsvpct))
	cursor.execute(agsql, agparams)

def writeOfficials(cursor, gameID, referee1ID, referee1Name, referee2ID, referee2Name, linesman1ID, linesman1Name, linesman2ID, linesman2Name):
	rsql = """INSERT INTO [Officials] ([GameID], [Referee1ID], [Referee1Name], [Referee2ID], [Referee2Name], [Linesman1ID], [Linesman1Name], [Linesman2ID], [Linesman2Name]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
	rparams= (str(gameID), str(referee1ID), referee1Name, str(referee2ID), referee2Name, str(linesman1ID), linesman1Name, str(linesman2ID), linesman2Name)
	cursor.execute(rsql, rparams)

def writeDecision(cursor, gameID, winner, loser):
	dsql = """INSERT INTO [Decision] ([GameID], [Winner], [Loser]) VALUES (?, ?, ?)"""
	dparams = (str(gameID), str(winner), str(loser))
	cursor.execute(dsql, dparams)

def writeStars(cursor, gameID, firstStar, secondStar, thirdStar):
	ssql = """INSERT INTO [Stars] ([GameID], [FirstStar], [SecondStar], [ThirdStar]) VALUES (?, ?, ?, ?)"""
	sparams = (str(gameID), str(firstStar), str(secondStar), str(thirdStar))
	cursor.execute(ssql, sparams)

def writeOnIce(cursor, gameID, period, time, event, situation, v1, v2, v3, v4, v5, v6, h1, h2, h3, h4, h5, h6):
	oisql = """INSERT INTO [OnIce] ([GameID], [Period], [Time], [Event], [Situation], [V1], [V2], [V3], [V4], [V5], [V6], [H1], [H2], [H3], [H4], [H5], [H6]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
	oiparams = (str(gameID), str(period), time, event, situation, str(v1), str(v2), str(v3), str(v4), str(v5), str(v6), str(h1), str(h2), str(h3), str(h4), str(h5), str(h6))
	cursor.execute(oisql, oiparams)