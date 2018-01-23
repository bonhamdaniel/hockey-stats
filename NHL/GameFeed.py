#GameFeed.py
import requests
from bs4 import BeautifulSoup

def getJSON(gameID):
	r = requests.get('http://statsapi.web.nhl.com/api/v1/game/' + gameID + '/feed/live')
	if r.status_code == 200:
		gameFile = r.json()
		return gameFile
	else:
		return None

def getHTML(season, gameID):
	r = requests.get('http://www.nhl.com/scores/htmlreports/' + season + '/PL0' + gameID + '.HTM')
	if r.status_code == 200:
		soup = BeautifulSoup(r.text, 'html.parser')
		return soup
	else:
		return None

def getGameInfo(gameFile):
	season = gameFile["gameData"]["game"]["season"].strip()
	seasonType = gameFile["gameData"]["game"]["type"].strip()
	date = gameFile["gameData"]["datetime"]["dateTime"].split("T")[0].strip()
	awayTeam = gameFile["gameData"]["teams"]["away"]["id"]
	homeTeam = gameFile["gameData"]["teams"]["home"]["id"]
	periods = gameFile["liveData"]["linescore"]["periods"]
	awaySide = 'unknown'
	homeSide = 'unknown'
	for p in range(0, len(periods)):
		if periods[p]["num"] == 1 and "rinkSide" in periods[p]["away"]:
			 awaySide = periods[p]["away"]["rinkSide"]
			 homeSide = periods[p]["home"]["rinkSide"]
	if len(periods) > 3:
		ot = 'yes'
	else:
		ot = 'no'
	so = gameFile["liveData"]["linescore"]["hasShootout"]
	return season, seasonType, date, awayTeam, homeTeam, awaySide, homeSide, ot, so

def getPlayers(gameFile):
	players = gameFile["gameData"]["players"]
	keys = {}
	i = 0
	for key, value in players.items():
		keys[i] = key
		i += 1
	return players, keys

def getEventType(events, event):
	return events[event]["result"]["event"]

def getFaceoff(events, event):
	team = events[event]["team"]["id"]
	winner = events[event]["players"][0]["player"]["id"]
	loser = events[event]["players"][1]["player"]["id"]
	period = events[event]["about"]["period"]
	time = events[event]["about"]["periodTime"].strip()
	awayGoals = events[event]["about"]["goals"]["away"]
	homeGoals = events[event]["about"]["goals"]["home"]
	xCoord = events[event]["coordinates"]["x"]
	yCoord = events[event]["coordinates"]["y"]
	return team, winner, loser, period, time, awayGoals, homeGoals, xCoord, yCoord

def getHit(events, event):
	team = events[event]["team"]["id"]
	hitter = events[event]["players"][0]["player"]["id"]
	hittee = events[event]["players"][1]["player"]["id"]
	period = events[event]["about"]["period"]
	time = events[event]["about"]["periodTime"].strip()
	awayGoals = events[event]["about"]["goals"]["away"]
	homeGoals = events[event]["about"]["goals"]["home"]
	if len(events[event]["coordinates"]) > 1:
		xCoord = events[event]["coordinates"]["x"]
		yCoord = events[event]["coordinates"]["y"]
	else:
		xCoord = -999
		yCoord = -999
	return team, hitter, hittee, period, time, awayGoals, homeGoals, xCoord, yCoord

def getGiveaway(events, event):
	team = events[event]["team"]["id"]
	culprit = events[event]["players"][0]["player"]["id"]
	period = events[event]["about"]["period"]
	time = events[event]["about"]["periodTime"].strip()
	awayGoals = events[event]["about"]["goals"]["away"]
	homeGoals = events[event]["about"]["goals"]["home"]
	if len(events[event]["coordinates"]) > 1:
		xCoord = events[event]["coordinates"]["x"]
		yCoord = events[event]["coordinates"]["y"]
	else:
		xCoord = -999
		yCoord = -999
	return team, culprit, period, time, awayGoals, homeGoals, xCoord, yCoord

def getShot(events, event):
	team = events[event]["team"]["id"]
	shooter = events[event]["players"][0]["player"]["id"]
	if len(events[event]["players"]) > 1:
		goalie = events[event]["players"][1]["player"]["id"]
	else:
		goalie = 0
	if "secondaryType" in events[event]["result"]:
		shot = events[event]["result"]["secondaryType"].strip()
	else:
		shot = 'not specified'
	period = events[event]["about"]["period"]
	time = events[event]["about"]["periodTime"].strip()
	awayGoals = events[event]["about"]["goals"]["away"]
	homeGoals = events[event]["about"]["goals"]["home"]
	if len(events[event]["coordinates"]) > 1:
		xCoord = events[event]["coordinates"]["x"]
		yCoord = events[event]["coordinates"]["y"]
	else:
		xCoord = -999
		yCoord = -999
	return team, shooter, goalie, shot, period, time, awayGoals, homeGoals, xCoord, yCoord

def getBlock(events, event):
	team = events[event]["team"]["id"]
	blocker = events[event]["players"][0]["player"]["id"]
	shooter = events[event]["players"][1]["player"]["id"]
	period = events[event]["about"]["period"]
	time = events[event]["about"]["periodTime"].strip()
	#time = int(time.split(":")[0]) + int(time.split(":")[1]) / 60
	awayGoals = events[event]["about"]["goals"]["away"]
	homeGoals = events[event]["about"]["goals"]["home"]
	if len(events[event]["coordinates"]) > 1:
		xCoord = events[event]["coordinates"]["x"]
		yCoord = events[event]["coordinates"]["y"]
	else:
		xCoord = -999
		yCoord = -999
	return team, blocker, shooter, period, time, awayGoals, homeGoals, xCoord, yCoord

def getMiss(events, event):
	team = events[event]["team"]["id"]
	culprit = events[event]["players"][0]["player"]["id"]
	period = events[event]["about"]["period"]
	time = events[event]["about"]["periodTime"].strip()
	#time = int(time.split(":")[0]) + int(time.split(":")[1]) / 60
	awayGoals = events[event]["about"]["goals"]["away"]
	homeGoals = events[event]["about"]["goals"]["home"]
	if len(events[event]["coordinates"]) > 1:
		xCoord = events[event]["coordinates"]["x"]
		yCoord = events[event]["coordinates"]["y"]
	else:
		xCoord = -999
		yCoord = -999
	return team, culprit, period, time, awayGoals, homeGoals, xCoord, yCoord

def getTakeaway(events, event):
	team = events[event]["team"]["id"]
	taker = events[event]["players"][0]["player"]["id"]
	period = events[event]["about"]["period"]
	time = events[event]["about"]["periodTime"].strip()
	#time = int(time.split(":")[0]) + int(time.split(":")[1]) / 60
	awayGoals = events[event]["about"]["goals"]["away"]
	homeGoals = events[event]["about"]["goals"]["home"]
	if len(events[event]["coordinates"]) > 1:
		xCoord = events[event]["coordinates"]["x"]
		yCoord = events[event]["coordinates"]["y"]
	else:
		xCoord = -999
		yCoord = -999
	return team, taker, period, time, awayGoals, homeGoals, xCoord, yCoord

def getPenalty(events, event):
	team = events[event]["team"]["id"]
	if "players" in events[event]:
		taker = events[event]["players"][0]["player"]["id"]
		if len(events[event]["players"]) > 1:
			drawer = events[event]["players"][1]["player"]["id"]
		else:
			drawer = 0
	else:
		taker = 0
		drawer = 0
	penalty = events[event]["result"]["secondaryType"].strip()
	minutes = events[event]["result"]["penaltyMinutes"]
	period = events[event]["about"]["period"]
	time = events[event]["about"]["periodTime"].strip()
	if 'M' in time or 'J' in time or int(time[:2]) > 20:
		time = "23:59"
	#time = int(time.split(":")[0]) + int(time.split(":")[1]) / 60
	awayGoals = events[event]["about"]["goals"]["away"]
	homeGoals = events[event]["about"]["goals"]["home"]
	if len(events[event]["coordinates"]) > 1:
		xCoord = events[event]["coordinates"]["x"]
		yCoord = events[event]["coordinates"]["y"]
	else:
		xCoord = -999
		yCoord = -999
	return team, taker, drawer, penalty, minutes, period, time, awayGoals, homeGoals, xCoord, yCoord

def getGoal(events, event):
	team = events[event]["team"]["id"]
	secondary = 0
	primary = 0
	for p in events[event]["players"]:
		if 'Scorer' in p['playerType']:
			scorer = p["player"]["id"]
		elif 'Assist' in p['playerType'] and primary == 0:
			primary = p["player"]["id"]
		elif 'Assist' in p['playerType']:
			secondary = p["player"]["id"]
	#if len(events[event]["players"]) > 1 and events[event]["players"][1]["playerType"] in "Assist":
	#	primary = events[event]["players"][1]["player"]["id"]
	#if len(events[event]["players"]) > 2 and events[event]["players"][2]["playerType"] in "Assist":
	#	secondary = events[event]["players"][2]["player"]["id"]
	goalie = 0
	if events[event]["players"][len(events[event]["players"])-1]["playerType"] in "Goalie":
		goalie = events[event]["players"][len(events[event]["players"])-1]["player"]["id"]
	if "secondaryType" in events[event]["result"]:
		shot = events[event]["result"]["secondaryType"].strip()
	else:
		shot = ''
	situation = events[event]["result"]["strength"]["code"].strip()
	if "gameWinningGoal" in events[event]["result"]:
		gwg = bool(events[event]["result"]["gameWinningGoal"])
	else:
		gwg = False
	if "emptyNet" in events[event]["result"]:
		en = bool(events[event]["result"]["emptyNet"])
	else:
		en = False
	period = events[event]["about"]["period"]
	time = events[event]["about"]["periodTime"].strip()
	#time = int(time.split(":")[0]) + int(time.split(":")[1]) / 60
	awayGoals = events[event]["about"]["goals"]["away"]
	homeGoals = events[event]["about"]["goals"]["home"]
	if len(events[event]["coordinates"]) > 1:
		xCoord = events[event]["coordinates"]["x"]
		yCoord = events[event]["coordinates"]["y"]
	else:
		xCoord = -999
		yCoord = -999
	return team, scorer, primary, secondary, goalie, shot, situation, gwg, en, period, time, awayGoals, homeGoals, xCoord, yCoord

def getTeamSummary(boxscore):
	awayInfo = boxscore["teams"]["away"]
	aTeam = awayInfo["team"]["id"]
	aGoals = awayInfo["teamStats"]["teamSkaterStats"]["goals"]
	aPIM = awayInfo["teamStats"]["teamSkaterStats"]["pim"]
	if "shots" in awayInfo["teamStats"]["teamSkaterStats"]:
		aShots = awayInfo["teamStats"]["teamSkaterStats"]["shots"]
	else:
		aShots = 0
	aPPG = awayInfo["teamStats"]["teamSkaterStats"]["powerPlayGoals"]
	if "powerPlayOpportunities" in awayInfo["teamStats"]["teamSkaterStats"]:
		aPPOPP = awayInfo["teamStats"]["teamSkaterStats"]["powerPlayOpportunities"]
	else:
		aPPOPP = 0
	if "blocked" in awayInfo["teamStats"]["teamSkaterStats"]:
		aBlocks = awayInfo["teamStats"]["teamSkaterStats"]["blocked"]
	else:
		aBlocks = 0
	if "takeaways" in awayInfo["teamStats"]["teamSkaterStats"]:
		aTA = awayInfo["teamStats"]["teamSkaterStats"]["takeaways"]
	else:
		aTA = 0
	if "giveaways" in awayInfo["teamStats"]["teamSkaterStats"]:
		aGA = awayInfo["teamStats"]["teamSkaterStats"]["giveaways"]
	else:
		aGA = 0
	if "hits" in awayInfo["teamStats"]["teamSkaterStats"]:
		aHits = awayInfo["teamStats"]["teamSkaterStats"]["hits"]
	else:
		aHits = 0
	homeInfo = boxscore["teams"]["home"]
	hTeam = homeInfo["team"]["id"]
	hGoals = homeInfo["teamStats"]["teamSkaterStats"]["goals"]
	hPIM = homeInfo["teamStats"]["teamSkaterStats"]["pim"]
	if "shots" in homeInfo["teamStats"]["teamSkaterStats"]:
		hShots = homeInfo["teamStats"]["teamSkaterStats"]["shots"]
	else:
		hShots = 0
	hPPG = homeInfo["teamStats"]["teamSkaterStats"]["powerPlayGoals"]
	if "powerPlayOpportunities" in homeInfo["teamStats"]["teamSkaterStats"]:
		hPPOPP = homeInfo["teamStats"]["teamSkaterStats"]["powerPlayOpportunities"]
	else:
		hPPOPP = 0
	if "blocked" in homeInfo["teamStats"]["teamSkaterStats"]:
		hBlocks = homeInfo["teamStats"]["teamSkaterStats"]["blocked"]
	else:
		hBlocks = 0
	if "takeaways" in homeInfo["teamStats"]["teamSkaterStats"]:
		hTA = homeInfo["teamStats"]["teamSkaterStats"]["takeaways"]
	else:
		hTA = 0
	if "giveaways" in homeInfo["teamStats"]["teamSkaterStats"]:
		hGA = homeInfo["teamStats"]["teamSkaterStats"]["giveaways"]
	else:
		hGA = 0
	if "hits" in homeInfo["teamStats"]["teamSkaterStats"]:
		hHits = homeInfo["teamStats"]["teamSkaterStats"]["hits"]
	else:
		hHits = 0
	return aTeam, aGoals, aPIM, aShots, aPPG, aPPOPP, aBlocks, aTA, aGA, aHits, hTeam, hGoals, hPIM, hShots, hPPG, hPPOPP, hBlocks, hTA, hGA, hHits

def getTeamPlayers(gameFile, team):
	teamID = gameFile["liveData"]["boxscore"]["teams"][team]["team"]["id"]
	players = gameFile["liveData"]["boxscore"]["teams"][team]["players"]
	keys = {}
	i = 0
	for key, value in players.items():
		keys[i] = key
		i += 1
	return teamID, players, keys

def getSkaterSummary(players, keys, player):
	if "jerseyNumber" in players[keys[player]]:
		no = players[keys[player]]["jerseyNumber"].strip()
		if no is "":
			no = -1
	else:
		no = -1
	toi = players[keys[player]]["stats"]["skaterStats"]["timeOnIce"].strip()
	toi = int(toi.split(":")[0]) + int(toi.split(":")[1]) / 60
	assists = players[keys[player]]["stats"]["skaterStats"]["assists"]
	goals = players[keys[player]]["stats"]["skaterStats"]["goals"]
	if "shots" in players[keys[player]]["stats"]["skaterStats"]:
		shots = players[keys[player]]["stats"]["skaterStats"]["shots"]
	else:
		shots = 0
	if "hits" in players[keys[player]]["stats"]["skaterStats"]:
		hits = players[keys[player]]["stats"]["skaterStats"]["hits"]
	else:
		hits = 0
	if "powerPlayGoals" in players[keys[player]]["stats"]["skaterStats"]:
		ppg = players[keys[player]]["stats"]["skaterStats"]["powerPlayGoals"]
	else:
		ppg = 0
	if "powerPlayAssists" in players[keys[player]]["stats"]["skaterStats"]:
		ppa = players[keys[player]]["stats"]["skaterStats"]["powerPlayAssists"]
	else:
		ppa = 0
	pim = players[keys[player]]["stats"]["skaterStats"]["penaltyMinutes"]
	if "faceOffWins" in players[keys[player]]["stats"]["skaterStats"]:
		fow = players[keys[player]]["stats"]["skaterStats"]["faceOffWins"]
	else:
		fow = 0
	if "faceoffTaken" in players[keys[player]]["stats"]["skaterStats"]:
		fot = players[keys[player]]["stats"]["skaterStats"]["faceoffTaken"]
	else:
		fot = 0
	if "takeaways" in players[keys[player]]["stats"]["skaterStats"]:
		ta = players[keys[player]]["stats"]["skaterStats"]["takeaways"]
	else:
		ta = 0
	if "giveaways" in players[keys[player]]["stats"]["skaterStats"]:
		ga = players[keys[player]]["stats"]["skaterStats"]["giveaways"]
	else:
		ga = 0
	if "shortHandedGoals" in players[keys[player]]["stats"]["skaterStats"]:
		shg = players[keys[player]]["stats"]["skaterStats"]["shortHandedGoals"]
	else:
		shg = 0
	if "shortHandedAssists" in players[keys[player]]["stats"]["skaterStats"]:
		sha = players[keys[player]]["stats"]["skaterStats"]["shortHandedAssists"]
	else:
		sha = 0
	if "blocked" in players[keys[player]]["stats"]["skaterStats"]:
		blocks = players[keys[player]]["stats"]["skaterStats"]["blocked"]
	else:
		blocks = 0
	if "plusMinus" in players[keys[player]]["stats"]["skaterStats"]:
		plusMinus = players[keys[player]]["stats"]["skaterStats"]["plusMinus"]
	else:
		plusMinus = 0
	if "evenTimeOnIce" in players[keys[player]]["stats"]["skaterStats"]:
		EVTOI = players[keys[player]]["stats"]["skaterStats"]["evenTimeOnIce"].strip()
		EVTOI = int(EVTOI.split(":")[0]) + int(EVTOI.split(":")[1]) / 60
	else:
		EVTOI = 0
	if "powerPlayTimeOnIce" in players[keys[player]]["stats"]["skaterStats"]:
		PPTOI = players[keys[player]]["stats"]["skaterStats"]["powerPlayTimeOnIce"].strip()
		PPTOI = int(PPTOI.split(":")[0]) + int(PPTOI.split(":")[1]) / 60
	else:
		PPTOI = 0
	if "shortHandedTimeOnIce" in players[keys[player]]["stats"]["skaterStats"]:
		SHTOI = players[keys[player]]["stats"]["skaterStats"]["shortHandedTimeOnIce"].strip()
		SHTOI = int(SHTOI.split(":")[0]) + int(SHTOI.split(":")[1]) / 60
	else:
		SHTOI = 0
	return no, toi, assists, goals, shots, hits, ppg, ppa, pim, fow, fot, ta, ga, shg, sha, blocks, plusMinus, EVTOI, PPTOI, SHTOI

def getGoalieSummary(players, keys, player):
	if "jerseyNumber" in players[keys[player]]:
		no = players[keys[player]]["jerseyNumber"].strip()
		if no is '':
			no = -1
	else:
		no = -1
	toi = players[keys[player]]["stats"]["goalieStats"]["timeOnIce"].strip()
	toi = int(toi.split(":")[0]) + int(toi.split(":")[1]) / 60
	assists = players[keys[player]]["stats"]["goalieStats"]["assists"]
	goals = players[keys[player]]["stats"]["goalieStats"]["goals"]
	pim = players[keys[player]]["stats"]["goalieStats"]["pim"]
	if "shots" in players[keys[player]]["stats"]["goalieStats"]:
		shots = players[keys[player]]["stats"]["goalieStats"]["shots"]
	else:
		shots = 0
	if "saves" in players[keys[player]]["stats"]["goalieStats"]:
		saves = players[keys[player]]["stats"]["goalieStats"]["saves"]
	else:
		saves = 0
	if "powerPlaySaves" in players[keys[player]]["stats"]["goalieStats"]:
		ppsv = players[keys[player]]["stats"]["goalieStats"]["powerPlaySaves"]
		shsv = players[keys[player]]["stats"]["goalieStats"]["shortHandedSaves"]
		evsv = players[keys[player]]["stats"]["goalieStats"]["evenSaves"]
		shsa = players[keys[player]]["stats"]["goalieStats"]["shortHandedShotsAgainst"]
		evsa = players[keys[player]]["stats"]["goalieStats"]["evenShotsAgainst"]
		ppsa = players[keys[player]]["stats"]["goalieStats"]["powerPlayShotsAgainst"]
	else:
		ppsv = 0
		shsv = 0
		evsv = 0
		shsa = 0
		evsa = 0
		ppsa = 0
	if "decision" in players[keys[player]]["stats"]["goalieStats"]:
		decision = players[keys[player]]["stats"]["goalieStats"]["decision"].strip()
	else:
		decision = ""
	if "savePercentage" in players[keys[player]]["stats"]["goalieStats"]:
		svpct = players[keys[player]]["stats"]["goalieStats"]["savePercentage"]
	else:
		svpct = 0
	if "evenStrengthSavePercentage" in players[keys[player]]["stats"]["goalieStats"]:
		evsvpct = players[keys[player]]["stats"]["goalieStats"]["evenStrengthSavePercentage"]
	else:
		evsvpct = 0
	return no, toi, assists, goals, pim, shots, saves, ppsv, shsv, evsv, shsa, evsa, ppsa, decision, svpct, evsvpct

def getOfficials(gameFile):
	officials = gameFile["liveData"]["boxscore"]["officials"]
	referees = [-999, -999]
	linesmen = [-999, -999]
	if 'id' in officials:
		refs = 0
		for i in range(0, len(officials)):
			if officials[i]["officialType"] in "Referee":
				referees[i] = officials[i]["official"]["id"]
				refs += 1
			elif officials[i]["officialType"] in "Linesman":
				linesmen[i-refs] = officials[i]["official"]["id"]
	return referees, linesmen

def getDecision(gameFile):
	decisions = gameFile["liveData"]["decisions"]
	winner = decisions["winner"]["id"]
	loser = decisions["loser"]["id"]
	return winner, loser

def getStars(gameFile):
	decisions = gameFile["liveData"]["decisions"]
	if len(decisions) > 2:
		firstStar = decisions["firstStar"]["id"]
		secondStar = decisions["secondStar"]["id"]
		thirdStar = decisions["thirdStar"]["id"]
	else:
		firstStar = -999
		secondStar = -999
		thirdStar = -999
	return firstStar, secondStar, thirdStar