import django_tables2 as tables
import itertools
from itertools import chain
from .models import NhlTeam, NhlTeamSummary, AhlSeason
from django.db.models import Q
from django.db import connection

class NhlTeamStats(tables.Table):
	rank = tables.Column(empty_values=(), verbose_name='#')
	team = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Team')

	def __init__(self, *args, **kwargs):
		super(NhlTeamStats, self).__init__(*args, **kwargs)
		self.counter = itertools.count()
		next(self.counter)

	def render_rank(self):
		return '%d' % next(self.counter)

class TimeMachineSkater(tables.Table):
	rank = tables.Column(empty_values=(), verbose_name='#')
	player = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Player')
	age = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Age')
	position = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Pos')
	season = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Season')
	gp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='GP')
	g = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='G')
	a = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='A')
	p = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='P')
	pim = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PIM')
	s = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='S')
	ggp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='S%')
	agp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='ESP')
	pgp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PPP')
	esg = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='ESG')
	esa = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='ESA')
	esp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='ESP')
	ppg = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PPG')
	ppa = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PPA')
	ppp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PPP')
	shg = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SHG')
	sha = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SHA')
	shp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SHP')
	gpm = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='G(+/-)')
	apm = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='A(+/-)')
	ppm = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='P(+/-)')

	def __init__(self, *args, **kwargs):
		super(TimeMachineSkater, self).__init__(*args, **kwargs)
		self.counter = itertools.count()
		next(self.counter)

	def render_rank(self):
		return '%d' % next(self.counter)

class NhlSkaterSummary(tables.Table):
	rank = tables.Column(empty_values=(), verbose_name='#')
	player = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Player')
	team = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Team')
	age = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Age')
	position = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Pos')
	season = tables.Column(attrs = {'td': {'class': 'leftDashedBorder'}}, verbose_name='Season')
	gp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='GP')
	g = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='G')
	a = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='A')
	p = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='P')
	pm = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='+/-')
	pim = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PIM')
	s = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='S')
	sp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='S%')
	esp = tables.Column(attrs = {'td': {'class': 'leftDashedBorder'}}, verbose_name='ESP')
	ppp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PPP')
	shp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SHP')
	h = tables.Column(attrs = {'td': {'class': 'leftDashedBorder'}}, verbose_name='H')
	bl = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='BL')
	ga = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='GA')
	ta = tables.Column(attrs = {'td': {'class': 'leftDashedBorder'}}, verbose_name='TA')
	fow = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='FOW')
	fol = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='FOL')
	fop = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='FO%')
	sog = tables.Column(attrs = {'td': {'class': 'leftDashedBorder'}}, verbose_name='SOG')
	soa = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SOA')
	sop = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SO%')
	toi = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='TOI')

	def __init__(self, *args, **kwargs):
		super(NhlSkaterSummary, self).__init__(*args, **kwargs)
		self.counter = itertools.count()
		next(self.counter)

	def render_rank(self):
		return '%d' % next(self.counter)

class AhlSkaterSummary(tables.Table):
	rank = tables.Column(empty_values=(), verbose_name='#')
	player = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Player')
	age = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Age')
	position = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Pos')
	season = tables.Column(attrs = {'td': {'class': 'leftDashedBorder'}}, verbose_name='Season')
	gp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='GP')
	g = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='G')
	a = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='A')
	p = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='P')
	pm = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='+/-')
	pim = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PIM')
	s = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='S')
	sp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='S%')
	esp = tables.Column(attrs = {'td': {'class': 'leftDashedBorder'}}, verbose_name='ESP')
	ppp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PPP')
	shp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SHP')
	sog = tables.Column(attrs = {'td': {'class': 'leftDashedBorder'}}, verbose_name='SOG')
	soa = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SOA')
	sop = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SO%')

	def __init__(self, *args, **kwargs):
		super(AhlSkaterSummary, self).__init__(*args, **kwargs)
		self.counter = itertools.count()
		next(self.counter)

	def render_rank(self):
		return '%d' % next(self.counter)

class AhlSkaterSummaryRates(tables.Table):
	rank = tables.Column(empty_values=(), verbose_name='#')
	player = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Player')
	season = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Season')
	position = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Pos')
	age = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Age')
	gp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='GP')
	g = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='G')
	a = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='A')
	p = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='P')
	pm = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='+/-')
	pim = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PIM')
	s = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='S')
	esp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='ESP')
	ppp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PPP')
	shp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SHP')

	def __init__(self, *args, **kwargs):
		super(AhlSkaterSummaryRates, self).__init__(*args, **kwargs)
		self.counter = itertools.count()
		next(self.counter)

	def render_rank(self):
		return '%d' % next(self.counter)

class AhlSkaterSummaryPercentiles(tables.Table):
	rank = tables.Column(empty_values=(), verbose_name='#')
	player = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Player')
	season = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Season')
	position = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Pos')
	age = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Age')
	gp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='GP')
	g = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='G')
	a = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='A')
	p = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='P')
	pm = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='+/-')
	pim = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PIM')
	s = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='S')
	sp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='S%')
	esp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='ESP')
	ppp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PPP')
	shp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SHP')
	sop = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SO%')

	def __init__(self, *args, **kwargs):
		super(AhlSkaterSummaryPercentiles, self).__init__(*args, **kwargs)
		self.counter = itertools.count()
		next(self.counter)

	def render_rank(self):
		return '%d' % next(self.counter)

class AhlOnIce(tables.Table):
	rank = tables.Column(empty_values=(), verbose_name='#')
	player = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Player')
	season = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Season')
	position = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Pos')
	age = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Age')
	gp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='GP')
	gf = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='GF')
	ga = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='GA')
	fa = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='F-A')
	esgf = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='ES GF')
	esga = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='ES GA')
	esfa = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='ES F-A')
	ppgf = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PP GF')
	ppga = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PP GA')
	ppfa = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PP F-A')
	shgf = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SH GF')
	shga = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SH GA')
	shfa = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SH F-A')
	engf = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='EN GF')
	enga = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='EN GA')
	enfa = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='EN F-A')

	def __init__(self, *args, **kwargs):
		super(AhlOnIce, self).__init__(*args, **kwargs)
		self.counter = itertools.count()
		next(self.counter)

	def render_rank(self):
		return '%d' % next(self.counter)

class AhlScoringSituation(tables.Table):
	rank = tables.Column(empty_values=(), verbose_name='#')
	player = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Player')
	season = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Season')
	position = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Pos')
	age = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='Age')
	gp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='GP')
	g = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='G')
	a1 = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='A1')
	a2 = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='A2')
	a = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='A')
	p = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='P')
	p1 = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='P1')
	esg = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='ESG')
	esa1 = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='ESA1')
	esa2 = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='ESA2')
	esa = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='ESA')
	esp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='ESP')
	esp1 = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='ESP1')
	ppg = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PPG')
	ppa1 = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PPA1')
	ppa2 = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PPA2')
	ppa = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PPA')
	ppp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PPP')
	ppp1 = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='PPP1')
	shg = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SHG')
	sha1 = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SHA1')
	sha2 = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SHA2')
	sha = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SHA')
	shp = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SHP')
	shp1 = tables.Column(attrs = {'td': {'class': 'center'}}, verbose_name='SHP1')

	def __init__(self, *args, **kwargs):
		super(AhlScoringSituation, self).__init__(*args, **kwargs)
		self.counter = itertools.count()
		next(self.counter)

	def render_rank(self):
		return '%d' % next(self.counter)

def summarizeTeamData(data):
	result = []
	with connection.cursor() as cursor:
		cursor.execute('SELECT * FROM ahl_onice')
		row = cursor.fetchall()
		for r in row:
			result.append({'team': r[0]})
	return result

def nhlSkaterSummary(season, maxSeason, positions, minGP, minAge, maxAge):
	result = []
	positions = int(positions)
	with connection.cursor() as cursor:
		if positions == 1:
			params = [season.start_date, maxSeason.start_date, str(minGP), str(minAge), str(maxAge)]
			cursor.execute('SELECT * FROM nhl_skater_summary_tot JOIN nhl_season ON nhl_skater_summary_tot.\"SEASON\" = nhl_season.season_id WHERE start_date >= %s AND start_date <= %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', params)
		elif positions == 2:
			cursor.execute('SELECT * FROM nhl_skater_summary_tot JOIN nhl_season ON nhl_skater_summary_tot.\"SEASON\" = nhl_season.season_id WHERE start_date >= %s AND start_date <= %s AND \"POS\" <> %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
		elif positions == 3:
			cursor.execute('SELECT * FROM nhl_skater_summary_tot JOIN nhl_season ON nhl_skater_summary_tot.\"SEASON\" = nhl_season.season_id WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
		elif positions == 4:
			cursor.execute('SELECT * FROM nhl_skater_summary_tot JOIN nhl_season ON nhl_skater_summary_tot.\"SEASON\" = nhl_season.season_id WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'C', str(minGP), str(minAge), str(maxAge)])
		elif positions == 5:
			cursor.execute('SELECT * FROM nhl_skater_summary_tot JOIN nhl_season ON nhl_skater_summary_tot.\"SEASON\" = nhl_season.season_id WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', str(minGP), str(minAge), str(maxAge)])
		elif positions == 6:
			cursor.execute('SELECT * FROM nhl_skater_summary_tot JOIN nhl_season ON nhl_skater_summary_tot.\"SEASON\" = nhl_season.season_id WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'RW', str(minGP), str(minAge), str(maxAge)])
		else:
			cursor.execute('SELECT * FROM nhl_skater_summary_tot JOIN nhl_season ON nhl_skater_summary_tot.\"SEASON\" = nhl_season.season_id WHERE start_date >= %s AND start_date <= %s AND (\"POS\" = %s OR \"POS\" = %s) AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', 'RW', str(minGP), str(minAge), str(maxAge)])
		stats = cursor.fetchall()
		for s in stats:
			if s[10] == 0: 
				sp = 0.0
			else:
				sp = round(s[6] / s[10] * 100, 1)
			if s[26] == 0:
				sop = 0.0
			else:
				sog = s[25]
				soa = s[26]
				sop = round(s[25] / s[26] * 100, 1)
			if s[24] == 0:
				fop = 0.0
			else:
				fow = s[23]
				foa = s[24]
				fol = foa-fow
				fop = round(s[23] / s[24] * 100, 1)
			result.append({'player':s[0], 'team':s[1], 'season':str(s[4])[0:4]+'-'+str(s[4])[6:], 'position':s[2], 'age':s[3], 'gp':s[5], 'g':s[6], 'a':s[7], 'p':s[6]+s[7], 'pm':s[8], 'pim':s[9], 's':s[10], 'sp':sp, 'esp':s[6]+s[7]-s[11]-s[12]-s[13]-s[14], 'ppp':s[11]+s[12], 'shp':s[13]+s[14], 'h':s[19], 'bl':s[20], 'ga':s[21], 'ta':s[22], 'fow':fow, 'fol':fol, 'fop':fop,'sog':sog, 'soa':soa, 'sop':sop, 'toi':round(s[15], 2)})
	return result

def ahlSkaterSummary(season, maxSeason, positions, minGP, minAge, maxAge):
	result = []
	positions = int(positions)
	with connection.cursor() as cursor:
		if positions == 1:
			params = [season.start_date, maxSeason.start_date, str(minGP), str(minAge), str(maxAge)]
			cursor.execute('SELECT * FROM ahl_skater_summary JOIN ahl_season ON ahl_skater_summary.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', params)
		elif positions == 2:
			cursor.execute('SELECT * FROM ahl_skater_summary JOIN ahl_season ON ahl_skater_summary.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" <> %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
		elif positions == 3:
			cursor.execute('SELECT * FROM ahl_skater_summary JOIN ahl_season ON ahl_skater_summary.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
		elif positions == 4:
			cursor.execute('SELECT * FROM ahl_skater_summary JOIN ahl_season ON ahl_skater_summary.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'C', str(minGP), str(minAge), str(maxAge)])
		elif positions == 5:
			cursor.execute('SELECT * FROM ahl_skater_summary JOIN ahl_season ON ahl_skater_summary.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', str(minGP), str(minAge), str(maxAge)])
		elif positions == 6:
			cursor.execute('SELECT * FROM ahl_skater_summary JOIN ahl_season ON ahl_skater_summary.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'RW', str(minGP), str(minAge), str(maxAge)])
		else:
			cursor.execute('SELECT * FROM ahl_skater_summary JOIN ahl_season ON ahl_skater_summary.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND (\"POS\" = %s OR \"POS\" = %s) AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', 'RW', str(minGP), str(minAge), str(maxAge)])
		stats = cursor.fetchall()
		for s in stats:
			if s[13] == 0: 
				sp = 0.0
			else:
				sp = round(s[5] / s[13] * 100, 1)
			if s[33] == 0:
				sop = 0.0
			else:
				sog = s[32]
				soa = s[33]
				sop = round(s[32] / s[33] * 100, 1)
			result.append({'player':s[0], 'season':s[3][0:8], 'position':s[1], 'age':s[2], 'gp':s[4], 'g':s[5], 'a':s[8], 'p':s[9], 'pm':s[11], 'pim':s[12], 's':s[13], 'sp':sp, 'esp':s[18], 'ppp':s[24], 'shp':s[30], 'sog':sog, 'soa':soa, 'sop':sop})
	return result

def ahlSkaterSummaryRates(season, maxSeason, positions, minGP, minAge, maxAge):
	result = []
	positions = int(positions)
	with connection.cursor() as cursor:
		if positions == 1:
			cursor.execute('SELECT * FROM ahl_skater_summary_rates JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, str(minGP), str(minAge), str(maxAge)])
		elif positions == 2:
			cursor.execute('SELECT * FROM ahl_skater_summary_rates JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" <> %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
		elif positions == 3:
			cursor.execute('SELECT * FROM ahl_skater_summary_rates JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
		elif positions == 4:
			cursor.execute('SELECT * FROM ahl_skater_summary_rates JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'C', str(minGP), str(minAge), str(maxAge)])
		elif positions == 5:
			cursor.execute('SELECT * FROM ahl_skater_summary_rates JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', str(minGP), str(minAge), str(maxAge)])
		elif positions == 6:
			cursor.execute('SELECT * FROM ahl_skater_summary_rates JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'RW', str(minGP), str(minAge), str(maxAge)])
		else:
			cursor.execute('SELECT * FROM ahl_skater_summary_rates JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND (\"POS\" = %s OR \"POS\" = %s) AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', 'RW', str(minGP), str(minAge), str(maxAge)])
		stats = cursor.fetchall()
		for s in stats:
			result.append({'player':s[0], 'season':s[3][0:8], 'position':s[1], 'age':s[2], 'gp':s[4], 'g':s[5], 'a':s[8], 'p':s[9], 'pm':s[11], 'pim':s[12], 's':s[13], 'esp':s[18], 'ppp':s[24], 'shp':s[30]})
	return result

def ahlSkaterSummaryPercentiles(season, maxSeason, positions, minGP, minAge, maxAge):
	result = []
	positions = int(positions)
	with connection.cursor() as cursor:
		if positions == 1:
			cursor.execute('SELECT ahl_skater_summary_rates.\"PLAYER\", ahl_skater_summary_rates.\"POS\", ahl_skater_summary_rates.\"AGE\", ahl_skater_summary_rates.\"SEASON\", ahl_skater_summary_rates.\"GP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"G/GP\") AS \"G\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A1/GP\") AS \"A1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A2/GP\") AS \"A2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A/GP\") AS \"A\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P/GP\") AS \"P\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P1/GP\") AS \"P1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"[+/-]/GP\") AS \"+/-\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PIM/GP\") AS \"PIM\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"S/GP\") AS \"S\", percent_rank() OVER (ORDER BY ahl_shooting.\"SP\") AS \"SP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESG/GP\") AS \"ESG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA1/GP\") AS \"ESA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA2/GP\") AS \"ESA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA/GP\") AS \"ESA\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP/GP\") AS \"ESP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP1/GP\") AS \"ESP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPG/GP\") AS \"PPG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA1/GP\") AS \"PPA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA2/GP\") AS \"PPA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA/GP\") AS \"PPA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP/GP\") AS \"PPP\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP1/GP\") AS \"PPP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHG/GP\") AS \"SHG\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA1/GP\") AS \"SHA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHA2/GP\") AS \"SHA2\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA/GP\") AS \"SHA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHP/GP\") AS \"SHP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHP1/GP\") AS \"SHP1\", percent_rank() OVER (ORDER BY ahl_shooting.\"SOP\") AS \"SOP\" FROM ahl_skater_summary_rates JOIN ahl_skater_summary ON ahl_skater_summary_rates.\"PLAYER\" = ahl_skater_summary.\"PLAYER\" AND ahl_skater_summary_rates.\"SEASON\" = ahl_skater_summary.\"SEASON\" JOIN ahl_shooting ON ahl_skater_summary.\"PLAYER\" = ahl_shooting.\"PLAYER\" AND ahl_skater_summary.\"SEASON\" = ahl_shooting.\"SEASON\" JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name  WHERE start_date >= %s AND start_date <= %s AND ahl_skater_summary.\"GP\" >= %s AND ahl_skater_summary.\"AGE\" > %s AND ahl_skater_summary.\"AGE\" < %s', [season.start_date, maxSeason.start_date, str(minGP), str(minAge), str(maxAge)])
		elif positions == 2:
			cursor.execute('SELECT ahl_skater_summary_rates.\"PLAYER\", ahl_skater_summary_rates.\"POS\", ahl_skater_summary_rates.\"AGE\", ahl_skater_summary_rates.\"SEASON\", ahl_skater_summary_rates.\"GP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"G/GP\") AS \"G\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A1/GP\") AS \"A1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A2/GP\") AS \"A2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A/GP\") AS \"A\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P/GP\") AS \"P\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P1/GP\") AS \"P1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"[+/-]/GP\") AS \"+/-\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PIM/GP\") AS \"PIM\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"S/GP\") AS \"S\", percent_rank() OVER (ORDER BY ahl_shooting.\"SP\") AS \"SP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESG/GP\") AS \"ESG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA1/GP\") AS \"ESA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA2/GP\") AS \"ESA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA/GP\") AS \"ESA\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP/GP\") AS \"ESP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP1/GP\") AS \"ESP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPG/GP\") AS \"PPG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA1/GP\") AS \"PPA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA2/GP\") AS \"PPA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA/GP\") AS \"PPA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP/GP\") AS \"PPP\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP1/GP\") AS \"PPP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHG/GP\") AS \"SHG\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA1/GP\") AS \"SHA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHA2/GP\") AS \"SHA2\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA/GP\") AS \"SHA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHP/GP\") AS \"SHP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHP1/GP\") AS \"SHP1\", percent_rank() OVER (ORDER BY ahl_shooting.\"SOP\") AS \"SOP\" FROM ahl_skater_summary_rates JOIN ahl_skater_summary ON ahl_skater_summary_rates.\"PLAYER\" = ahl_skater_summary.\"PLAYER\" AND ahl_skater_summary_rates.\"SEASON\" = ahl_skater_summary.\"SEASON\" JOIN ahl_shooting ON ahl_skater_summary.\"PLAYER\" = ahl_shooting.\"PLAYER\" AND ahl_skater_summary.\"SEASON\" = ahl_shooting.\"SEASON\" JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name  WHERE start_date >= %s AND start_date <= %s AND ahl_skater_summary.\"POS\" <> %s AND ahl_skater_summary.\"GP\" >= %s AND ahl_skater_summary.\"AGE\" > %s AND ahl_skater_summary.\"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
		elif positions == 3:
			cursor.execute('SELECT ahl_skater_summary_rates.\"PLAYER\", ahl_skater_summary_rates.\"POS\", ahl_skater_summary_rates.\"AGE\", ahl_skater_summary_rates.\"SEASON\", ahl_skater_summary_rates.\"GP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"G/GP\") AS \"G\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A1/GP\") AS \"A1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A2/GP\") AS \"A2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A/GP\") AS \"A\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P/GP\") AS \"P\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P1/GP\") AS \"P1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"[+/-]/GP\") AS \"+/-\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PIM/GP\") AS \"PIM\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"S/GP\") AS \"S\", percent_rank() OVER (ORDER BY ahl_shooting.\"SP\") AS \"SP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESG/GP\") AS \"ESG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA1/GP\") AS \"ESA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA2/GP\") AS \"ESA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA/GP\") AS \"ESA\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP/GP\") AS \"ESP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP1/GP\") AS \"ESP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPG/GP\") AS \"PPG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA1/GP\") AS \"PPA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA2/GP\") AS \"PPA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA/GP\") AS \"PPA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP/GP\") AS \"PPP\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP1/GP\") AS \"PPP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHG/GP\") AS \"SHG\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA1/GP\") AS \"SHA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHA2/GP\") AS \"SHA2\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA/GP\") AS \"SHA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHP/GP\") AS \"SHP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHP1/GP\") AS \"SHP1\", percent_rank() OVER (ORDER BY ahl_shooting.\"SOP\") AS \"SOP\" FROM ahl_skater_summary_rates JOIN ahl_skater_summary ON ahl_skater_summary_rates.\"PLAYER\" = ahl_skater_summary.\"PLAYER\" AND ahl_skater_summary_rates.\"SEASON\" = ahl_skater_summary.\"SEASON\" JOIN ahl_shooting ON ahl_skater_summary.\"PLAYER\" = ahl_shooting.\"PLAYER\" AND ahl_skater_summary.\"SEASON\" = ahl_shooting.\"SEASON\" JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name  WHERE start_date >= %s AND start_date <= %s AND ahl_skater_summary.\"POS\" = %s AND ahl_skater_summary.\"GP\" >= %s AND ahl_skater_summary.\"AGE\" > %s AND ahl_skater_summary.\"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
		elif positions == 4:
			cursor.execute('SELECT ahl_skater_summary_rates.\"PLAYER\", ahl_skater_summary_rates.\"POS\", ahl_skater_summary_rates.\"AGE\", ahl_skater_summary_rates.\"SEASON\", ahl_skater_summary_rates.\"GP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"G/GP\") AS \"G\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A1/GP\") AS \"A1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A2/GP\") AS \"A2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A/GP\") AS \"A\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P/GP\") AS \"P\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P1/GP\") AS \"P1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"[+/-]/GP\") AS \"+/-\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PIM/GP\") AS \"PIM\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"S/GP\") AS \"S\", percent_rank() OVER (ORDER BY ahl_shooting.\"SP\") AS \"SP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESG/GP\") AS \"ESG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA1/GP\") AS \"ESA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA2/GP\") AS \"ESA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA/GP\") AS \"ESA\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP/GP\") AS \"ESP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP1/GP\") AS \"ESP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPG/GP\") AS \"PPG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA1/GP\") AS \"PPA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA2/GP\") AS \"PPA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA/GP\") AS \"PPA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP/GP\") AS \"PPP\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP1/GP\") AS \"PPP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHG/GP\") AS \"SHG\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA1/GP\") AS \"SHA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHA2/GP\") AS \"SHA2\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA/GP\") AS \"SHA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHP/GP\") AS \"SHP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHP1/GP\") AS \"SHP1\", percent_rank() OVER (ORDER BY ahl_shooting.\"SOP\") AS \"SOP\" FROM ahl_skater_summary_rates JOIN ahl_skater_summary ON ahl_skater_summary_rates.\"PLAYER\" = ahl_skater_summary.\"PLAYER\" AND ahl_skater_summary_rates.\"SEASON\" = ahl_skater_summary.\"SEASON\" JOIN ahl_shooting ON ahl_skater_summary.\"PLAYER\" = ahl_shooting.\"PLAYER\" AND ahl_skater_summary.\"SEASON\" = ahl_shooting.\"SEASON\" JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name  WHERE start_date >= %s AND start_date <= %s AND ahl_skater_summary.\"POS\" = %s AND ahl_skater_summary.\"GP\" >= %s AND ahl_skater_summary.\"AGE\" > %s AND ahl_skater_summary.\"AGE\" < %s', [season.start_date, maxSeason.start_date, 'C', str(minGP), str(minAge), str(maxAge)])				
		elif positions == 5:
			cursor.execute('SELECT ahl_skater_summary_rates.\"PLAYER\", ahl_skater_summary_rates.\"POS\", ahl_skater_summary_rates.\"AGE\", ahl_skater_summary_rates.\"SEASON\", ahl_skater_summary_rates.\"GP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"G/GP\") AS \"G\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A1/GP\") AS \"A1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A2/GP\") AS \"A2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A/GP\") AS \"A\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P/GP\") AS \"P\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P1/GP\") AS \"P1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"[+/-]/GP\") AS \"+/-\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PIM/GP\") AS \"PIM\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"S/GP\") AS \"S\", percent_rank() OVER (ORDER BY ahl_shooting.\"SP\") AS \"SP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESG/GP\") AS \"ESG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA1/GP\") AS \"ESA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA2/GP\") AS \"ESA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA/GP\") AS \"ESA\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP/GP\") AS \"ESP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP1/GP\") AS \"ESP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPG/GP\") AS \"PPG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA1/GP\") AS \"PPA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA2/GP\") AS \"PPA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA/GP\") AS \"PPA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP/GP\") AS \"PPP\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP1/GP\") AS \"PPP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHG/GP\") AS \"SHG\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA1/GP\") AS \"SHA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHA2/GP\") AS \"SHA2\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA/GP\") AS \"SHA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHP/GP\") AS \"SHP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHP1/GP\") AS \"SHP1\", percent_rank() OVER (ORDER BY ahl_shooting.\"SOP\") AS \"SOP\" FROM ahl_skater_summary_rates JOIN ahl_skater_summary ON ahl_skater_summary_rates.\"PLAYER\" = ahl_skater_summary.\"PLAYER\" AND ahl_skater_summary_rates.\"SEASON\" = ahl_skater_summary.\"SEASON\" JOIN ahl_shooting ON ahl_skater_summary.\"PLAYER\" = ahl_shooting.\"PLAYER\" AND ahl_skater_summary.\"SEASON\" = ahl_shooting.\"SEASON\" JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name  WHERE start_date >= %s AND start_date <= %s AND ahl_skater_summary.\"POS\" = %s AND ahl_skater_summary.\"GP\" >= %s AND ahl_skater_summary.\"AGE\" > %s AND ahl_skater_summary.\"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', str(minGP), str(minAge), str(maxAge)])
		elif positions == 6:
			cursor.execute('SELECT ahl_skater_summary_rates.\"PLAYER\", ahl_skater_summary_rates.\"POS\", ahl_skater_summary_rates.\"AGE\", ahl_skater_summary_rates.\"SEASON\", ahl_skater_summary_rates.\"GP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"G/GP\") AS \"G\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A1/GP\") AS \"A1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A2/GP\") AS \"A2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A/GP\") AS \"A\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P/GP\") AS \"P\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P1/GP\") AS \"P1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"[+/-]/GP\") AS \"+/-\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PIM/GP\") AS \"PIM\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"S/GP\") AS \"S\", percent_rank() OVER (ORDER BY ahl_shooting.\"SP\") AS \"SP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESG/GP\") AS \"ESG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA1/GP\") AS \"ESA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA2/GP\") AS \"ESA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA/GP\") AS \"ESA\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP/GP\") AS \"ESP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP1/GP\") AS \"ESP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPG/GP\") AS \"PPG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA1/GP\") AS \"PPA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA2/GP\") AS \"PPA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA/GP\") AS \"PPA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP/GP\") AS \"PPP\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP1/GP\") AS \"PPP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHG/GP\") AS \"SHG\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA1/GP\") AS \"SHA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHA2/GP\") AS \"SHA2\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA/GP\") AS \"SHA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHP/GP\") AS \"SHP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHP1/GP\") AS \"SHP1\", percent_rank() OVER (ORDER BY ahl_shooting.\"SOP\") AS \"SOP\" FROM ahl_skater_summary_rates JOIN ahl_skater_summary ON ahl_skater_summary_rates.\"PLAYER\" = ahl_skater_summary.\"PLAYER\" AND ahl_skater_summary_rates.\"SEASON\" = ahl_skater_summary.\"SEASON\" JOIN ahl_shooting ON ahl_skater_summary.\"PLAYER\" = ahl_shooting.\"PLAYER\" AND ahl_skater_summary.\"SEASON\" = ahl_shooting.\"SEASON\" JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name  WHERE start_date >= %s AND start_date <= %s AND ahl_skater_summary.\"POS\" = %s AND ahl_skater_summary.\"GP\" >= %s AND ahl_skater_summary.\"AGE\" > %s AND ahl_skater_summary.\"AGE\" < %s', [season.start_date, maxSeason.start_date, 'RW', str(minGP), str(minAge), str(maxAge)])				
		else:
			cursor.execute('SELECT ahl_skater_summary_rates.\"PLAYER\", ahl_skater_summary_rates.\"POS\", ahl_skater_summary_rates.\"AGE\", ahl_skater_summary_rates.\"SEASON\", ahl_skater_summary_rates.\"GP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"G/GP\") AS \"G\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A1/GP\") AS \"A1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A2/GP\") AS \"A2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A/GP\") AS \"A\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P/GP\") AS \"P\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P1/GP\") AS \"P1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"[+/-]/GP\") AS \"+/-\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PIM/GP\") AS \"PIM\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"S/GP\") AS \"S\", percent_rank() OVER (ORDER BY ahl_shooting.\"SP\") AS \"SP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESG/GP\") AS \"ESG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA1/GP\") AS \"ESA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA2/GP\") AS \"ESA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA/GP\") AS \"ESA\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP/GP\") AS \"ESP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP1/GP\") AS \"ESP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPG/GP\") AS \"PPG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA1/GP\") AS \"PPA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA2/GP\") AS \"PPA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA/GP\") AS \"PPA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP/GP\") AS \"PPP\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP1/GP\") AS \"PPP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHG/GP\") AS \"SHG\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA1/GP\") AS \"SHA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHA2/GP\") AS \"SHA2\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA/GP\") AS \"SHA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHP/GP\") AS \"SHP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHP1/GP\") AS \"SHP1\", percent_rank() OVER (ORDER BY ahl_shooting.\"SOP\") AS \"SOP\" FROM ahl_skater_summary_rates JOIN ahl_skater_summary ON ahl_skater_summary_rates.\"PLAYER\" = ahl_skater_summary.\"PLAYER\" AND ahl_skater_summary_rates.\"SEASON\" = ahl_skater_summary.\"SEASON\" JOIN ahl_shooting ON ahl_skater_summary.\"PLAYER\" = ahl_shooting.\"PLAYER\" AND ahl_skater_summary.\"SEASON\" = ahl_shooting.\"SEASON\" JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name  WHERE start_date >= %s AND start_date <= %s AND (ahl_skater_summary.\"POS\" = %s OR ahl_skater_summary.\"POS\" = %s) AND ahl_skater_summary.\"GP\" >= %s AND ahl_skater_summary.\"AGE\" > %s AND ahl_skater_summary.\"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', 'RW', str(minGP), str(minAge), str(maxAge)])				
		stats = cursor.fetchall()
		for s in stats:
			result.append({'player':s[0], 'season':s[3][0:8], 'position':s[1], 'age':s[2], 'gp':s[4], 'g':round(s[5]*100, 1), 'a':round(s[8]*100, 1), 'p':round(s[9]*100, 1), 'pm':round(s[11]*100, 1), 'pim':round(s[12]*100, 1), 's':round(s[13]*100, 1), 'sp':round(s[14]*100, 1), 'esp':round(s[19]*100, 1), 'ppp':round(s[25]*100, 1), 'shp':round(s[31]*100, 1), 'sop':round(s[33]*100, 1)})
	return result

def ahlOnIce(season, maxSeason, positions, report, minGP, minAge, maxAge):
	result = []
	positions = int(positions)
	report = int(report)
	with connection.cursor() as cursor:
		if positions == 1:
			if report-4 == 0:
				cursor.execute('SELECT * FROM ahl_onice JOIN ahl_season ON ahl_onice.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, str(minGP), str(minAge), str(maxAge)])
			elif report-4 == 1:
				cursor.execute('SELECT * FROM ahl_onice_rates JOIN ahl_season ON ahl_onice_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, str(minGP), str(minAge), str(maxAge)])
			else:
				cursor.execute('SELECT ahl_onice_rates."PLAYER", ahl_onice_rates."POS", ahl_onice_rates."AGE", ahl_onice_rates."SEASON", ahl_onice_rates."GP", percent_rank() OVER (ORDER BY ahl_onice_rates."GF") AS "GF", percent_rank() OVER (ORDER BY ahl_onice_rates."GA" DESC) AS "GA", percent_rank() OVER (ORDER BY ahl_onice_rates."GF-GA") AS "GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."ESGF") AS "ESGF", percent_rank() OVER (ORDER BY ahl_onice_rates."ESGA" DESC) AS "ESGA", percent_rank() OVER (ORDER BY ahl_onice_rates."ES GF-GA") AS "ES GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."PPGF") AS "PPGF", cume_dist() OVER (ORDER BY ahl_onice_rates."PPGA" DESC) AS "PPGA", percent_rank() OVER (ORDER BY ahl_onice_rates."PP GF-GA") AS "PP GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."SHGF") AS "SHGF", cume_dist() OVER (ORDER BY ahl_onice_rates."SHGA" DESC) AS "SHGA", percent_rank() OVER (ORDER BY ahl_onice_rates."SH GF-GA") AS "SH GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."ENGF") AS "ENGF", cume_dist() OVER (ORDER BY ahl_onice_rates."ENGA" DESC) AS "ENGA", percent_rank() OVER (ORDER BY ahl_onice_rates."EN GF-GA") AS "EN GF-GA" FROM ahl_onice_rates JOIN ahl_season ON ahl_onice_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, str(minGP), str(minAge), str(maxAge)])
		elif positions == 2:
			if report-4 == 0:
				cursor.execute('SELECT * FROM ahl_onice JOIN ahl_season ON ahl_onice.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" <> %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
			elif report-4 == 1:
				cursor.execute('SELECT * FROM ahl_onice_rates JOIN ahl_season ON ahl_onice_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" <> %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
			else:
				cursor.execute('SELECT ahl_onice_rates."PLAYER", ahl_onice_rates."POS", ahl_onice_rates."AGE", ahl_onice_rates."SEASON", ahl_onice_rates."GP", percent_rank() OVER (ORDER BY ahl_onice_rates."GF") AS "GF", percent_rank() OVER (ORDER BY ahl_onice_rates."GA" DESC) AS "GA", percent_rank() OVER (ORDER BY ahl_onice_rates."GF-GA") AS "GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."ESGF") AS "ESGF", percent_rank() OVER (ORDER BY ahl_onice_rates."ESGA" DESC) AS "ESGA", percent_rank() OVER (ORDER BY ahl_onice_rates."ES GF-GA") AS "ES GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."PPGF") AS "PPGF", cume_dist() OVER (ORDER BY ahl_onice_rates."PPGA" DESC) AS "PPGA", percent_rank() OVER (ORDER BY ahl_onice_rates."PP GF-GA") AS "PP GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."SHGF") AS "SHGF", cume_dist() OVER (ORDER BY ahl_onice_rates."SHGA" DESC) AS "SHGA", percent_rank() OVER (ORDER BY ahl_onice_rates."SH GF-GA") AS "SH GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."ENGF") AS "ENGF", cume_dist() OVER (ORDER BY ahl_onice_rates."ENGA" DESC) AS "ENGA", percent_rank() OVER (ORDER BY ahl_onice_rates."EN GF-GA") AS "EN GF-GA" FROM ahl_onice_rates JOIN ahl_season ON ahl_onice_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" <> %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
		elif positions == 3:
			if report-4 == 0:
				cursor.execute('SELECT * FROM ahl_onice JOIN ahl_season ON ahl_onice.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
			elif report-4 == 1:
				cursor.execute('SELECT * FROM ahl_onice_rates JOIN ahl_season ON ahl_onice_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
			else:
				cursor.execute('SELECT ahl_onice_rates."PLAYER", ahl_onice_rates."POS", ahl_onice_rates."AGE", ahl_onice_rates."SEASON", ahl_onice_rates."GP", percent_rank() OVER (ORDER BY ahl_onice_rates."GF") AS "GF", percent_rank() OVER (ORDER BY ahl_onice_rates."GA" DESC) AS "GA", percent_rank() OVER (ORDER BY ahl_onice_rates."GF-GA") AS "GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."ESGF") AS "ESGF", percent_rank() OVER (ORDER BY ahl_onice_rates."ESGA" DESC) AS "ESGA", percent_rank() OVER (ORDER BY ahl_onice_rates."ES GF-GA") AS "ES GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."PPGF") AS "PPGF", cume_dist() OVER (ORDER BY ahl_onice_rates."PPGA" DESC) AS "PPGA", percent_rank() OVER (ORDER BY ahl_onice_rates."PP GF-GA") AS "PP GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."SHGF") AS "SHGF", cume_dist() OVER (ORDER BY ahl_onice_rates."SHGA" DESC) AS "SHGA", percent_rank() OVER (ORDER BY ahl_onice_rates."SH GF-GA") AS "SH GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."ENGF") AS "ENGF", cume_dist() OVER (ORDER BY ahl_onice_rates."ENGA" DESC) AS "ENGA", percent_rank() OVER (ORDER BY ahl_onice_rates."EN GF-GA") AS "EN GF-GA" FROM ahl_onice_rates JOIN ahl_season ON ahl_onice_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
		elif positions == 4:
			if report-4 == 0:
				cursor.execute('SELECT * FROM ahl_onice JOIN ahl_season ON ahl_onice.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'C', str(minGP), str(minAge), str(maxAge)])
			elif report-4 == 1:
				cursor.execute('SELECT * FROM ahl_onice_rates JOIN ahl_season ON ahl_onice_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'C', str(minGP), str(minAge), str(maxAge)])
			else:
				cursor.execute('SELECT ahl_onice_rates."PLAYER", ahl_onice_rates."POS", ahl_onice_rates."AGE", ahl_onice_rates."SEASON", ahl_onice_rates."GP", percent_rank() OVER (ORDER BY ahl_onice_rates."GF") AS "GF", percent_rank() OVER (ORDER BY ahl_onice_rates."GA" DESC) AS "GA", percent_rank() OVER (ORDER BY ahl_onice_rates."GF-GA") AS "GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."ESGF") AS "ESGF", percent_rank() OVER (ORDER BY ahl_onice_rates."ESGA" DESC) AS "ESGA", percent_rank() OVER (ORDER BY ahl_onice_rates."ES GF-GA") AS "ES GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."PPGF") AS "PPGF", cume_dist() OVER (ORDER BY ahl_onice_rates."PPGA" DESC) AS "PPGA", percent_rank() OVER (ORDER BY ahl_onice_rates."PP GF-GA") AS "PP GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."SHGF") AS "SHGF", cume_dist() OVER (ORDER BY ahl_onice_rates."SHGA" DESC) AS "SHGA", percent_rank() OVER (ORDER BY ahl_onice_rates."SH GF-GA") AS "SH GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."ENGF") AS "ENGF", cume_dist() OVER (ORDER BY ahl_onice_rates."ENGA" DESC) AS "ENGA", percent_rank() OVER (ORDER BY ahl_onice_rates."EN GF-GA") AS "EN GF-GA" FROM ahl_onice_rates JOIN ahl_season ON ahl_onice_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'C', str(minGP), str(minAge), str(maxAge)])
		elif positions == 5:
			if report-4 == 0:
				cursor.execute('SELECT * FROM ahl_onice JOIN ahl_season ON ahl_onice.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', str(minGP), str(minAge), str(maxAge)])
			elif report-4 == 1:
				cursor.execute('SELECT * FROM ahl_onice_rates JOIN ahl_season ON ahl_onice_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', str(minGP), str(minAge), str(maxAge)])
			else:
				cursor.execute('SELECT ahl_onice_rates."PLAYER", ahl_onice_rates."POS", ahl_onice_rates."AGE", ahl_onice_rates."SEASON", ahl_onice_rates."GP", percent_rank() OVER (ORDER BY ahl_onice_rates."GF") AS "GF", percent_rank() OVER (ORDER BY ahl_onice_rates."GA" DESC) AS "GA", percent_rank() OVER (ORDER BY ahl_onice_rates."GF-GA") AS "GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."ESGF") AS "ESGF", percent_rank() OVER (ORDER BY ahl_onice_rates."ESGA" DESC) AS "ESGA", percent_rank() OVER (ORDER BY ahl_onice_rates."ES GF-GA") AS "ES GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."PPGF") AS "PPGF", cume_dist() OVER (ORDER BY ahl_onice_rates."PPGA" DESC) AS "PPGA", percent_rank() OVER (ORDER BY ahl_onice_rates."PP GF-GA") AS "PP GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."SHGF") AS "SHGF", cume_dist() OVER (ORDER BY ahl_onice_rates."SHGA" DESC) AS "SHGA", percent_rank() OVER (ORDER BY ahl_onice_rates."SH GF-GA") AS "SH GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."ENGF") AS "ENGF", cume_dist() OVER (ORDER BY ahl_onice_rates."ENGA" DESC) AS "ENGA", percent_rank() OVER (ORDER BY ahl_onice_rates."EN GF-GA") AS "EN GF-GA" FROM ahl_onice_rates JOIN ahl_season ON ahl_onice_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', str(minGP), str(minAge), str(maxAge)])
		elif positions == 6:
			if report-4 == 0:
				cursor.execute('SELECT * FROM ahl_onice JOIN ahl_season ON ahl_onice.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'RW', str(minGP), str(minAge), str(maxAge)])
			elif report-4 == 1:
				cursor.execute('SELECT * FROM ahl_onice_rates JOIN ahl_season ON ahl_onice_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'RW', str(minGP), str(minAge), str(maxAge)])
			else:
				cursor.execute('SELECT ahl_onice_rates."PLAYER", ahl_onice_rates."POS", ahl_onice_rates."AGE", ahl_onice_rates."SEASON", ahl_onice_rates."GP", percent_rank() OVER (ORDER BY ahl_onice_rates."GF") AS "GF", percent_rank() OVER (ORDER BY ahl_onice_rates."GA" DESC) AS "GA", percent_rank() OVER (ORDER BY ahl_onice_rates."GF-GA") AS "GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."ESGF") AS "ESGF", percent_rank() OVER (ORDER BY ahl_onice_rates."ESGA" DESC) AS "ESGA", percent_rank() OVER (ORDER BY ahl_onice_rates."ES GF-GA") AS "ES GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."PPGF") AS "PPGF", cume_dist() OVER (ORDER BY ahl_onice_rates."PPGA" DESC) AS "PPGA", percent_rank() OVER (ORDER BY ahl_onice_rates."PP GF-GA") AS "PP GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."SHGF") AS "SHGF", cume_dist() OVER (ORDER BY ahl_onice_rates."SHGA" DESC) AS "SHGA", percent_rank() OVER (ORDER BY ahl_onice_rates."SH GF-GA") AS "SH GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."ENGF") AS "ENGF", cume_dist() OVER (ORDER BY ahl_onice_rates."ENGA" DESC) AS "ENGA", percent_rank() OVER (ORDER BY ahl_onice_rates."EN GF-GA") AS "EN GF-GA" FROM ahl_onice_rates JOIN ahl_season ON ahl_onice_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'RW', str(minGP), str(minAge), str(maxAge)])
		else:
			if report-4 == 0:
				cursor.execute('SELECT * FROM ahl_onice JOIN ahl_season ON ahl_onice.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND (\"POS\" = %s OR \"POS\" = %s) AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', 'RW', str(minGP), str(minAge), str(maxAge)])
			elif report-4 == 1:
				cursor.execute('SELECT * FROM ahl_onice_rates JOIN ahl_season ON ahl_onice_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND (\"POS\" = %s OR \"POS\" = %s) AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', 'RW', str(minGP), str(minAge), str(maxAge)])
			else:
				cursor.execute('SELECT ahl_onice_rates."PLAYER", ahl_onice_rates."POS", ahl_onice_rates."AGE", ahl_onice_rates."SEASON", ahl_onice_rates."GP", percent_rank() OVER (ORDER BY ahl_onice_rates."GF") AS "GF", percent_rank() OVER (ORDER BY ahl_onice_rates."GA" DESC) AS "GA", percent_rank() OVER (ORDER BY ahl_onice_rates."GF-GA") AS "GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."ESGF") AS "ESGF", percent_rank() OVER (ORDER BY ahl_onice_rates."ESGA" DESC) AS "ESGA", percent_rank() OVER (ORDER BY ahl_onice_rates."ES GF-GA") AS "ES GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."PPGF") AS "PPGF", cume_dist() OVER (ORDER BY ahl_onice_rates."PPGA" DESC) AS "PPGA", percent_rank() OVER (ORDER BY ahl_onice_rates."PP GF-GA") AS "PP GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."SHGF") AS "SHGF", cume_dist() OVER (ORDER BY ahl_onice_rates."SHGA" DESC) AS "SHGA", percent_rank() OVER (ORDER BY ahl_onice_rates."SH GF-GA") AS "SH GF-GA", percent_rank() OVER (ORDER BY ahl_onice_rates."ENGF") AS "ENGF", cume_dist() OVER (ORDER BY ahl_onice_rates."ENGA" DESC) AS "ENGA", percent_rank() OVER (ORDER BY ahl_onice_rates."EN GF-GA") AS "EN GF-GA" FROM ahl_onice_rates JOIN ahl_season ON ahl_onice_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND (\"POS\" = %s OR \"POS\" = %s) AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', 'RW', str(minGP), str(minAge), str(maxAge)])
		stats = cursor.fetchall()
		for s in stats:
			s = list(s)
			if report-4 == 2:
				for i in range(5, 20):
					s[i] = round(s[i]*100, 1)
			result.append({'player':s[0], 'season':s[3][0:8], 'position':s[1], 'age':s[2], 'gp':s[4], 'gf':s[5], 'ga':s[6], 'fa':s[7], 'esgf':s[8], 'esga':s[9], 'esfa':s[10], 'ppgf':s[11], 'ppga':s[12], 'ppfa':s[13], 'shgf':s[14], 'shga':s[15], 'shfa':s[16], 'engf':s[17], 'enga':s[18], 'enfa':s[19]})
	return result

def ahlScoringSituation(season, maxSeason, positions, report, minGP, minAge, maxAge):
	result = []
	positions = int(positions)
	report = int(report)
	with connection.cursor() as cursor:
		if positions == 1:
			if report == 7:
				cursor.execute('SELECT * FROM ahl_skater_summary JOIN ahl_season ON ahl_skater_summary.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, str(minGP), str(minAge), str(maxAge)])
			elif report == 8:
				cursor.execute('SELECT * FROM ahl_skater_summary_rates JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, str(minGP), str(minAge), str(maxAge)])
			else:
				cursor.execute('SELECT ahl_skater_summary_rates.\"PLAYER\", ahl_skater_summary_rates.\"POS\", ahl_skater_summary_rates.\"AGE\", ahl_skater_summary_rates.\"SEASON\", ahl_skater_summary_rates.\"GP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"G/GP\") AS \"G\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A1/GP\") AS \"A1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A2/GP\") AS \"A2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A/GP\") AS \"A\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P/GP\") AS \"P\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P1/GP\") AS \"P1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"[+/-]/GP\") AS \"+/-\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PIM/GP\") AS \"PIM\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"S/GP\") AS \"S\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESG/GP\") AS \"ESG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA1/GP\") AS \"ESA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA2/GP\") AS \"ESA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA/GP\") AS \"ESA\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP/GP\") AS \"ESP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP1/GP\") AS \"ESP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPG/GP\") AS \"PPG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA1/GP\") AS \"PPA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA2/GP\") AS \"PPA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA/GP\") AS \"PPA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP/GP\") AS \"PPP\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP1/GP\") AS \"PPP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHG/GP\") AS \"SHG\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA1/GP\") AS \"SHA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHA2/GP\") AS \"SHA2\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA/GP\") AS \"SHA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHP/GP\") AS \"SHP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHP1/GP\") AS \"SHP1\" FROM ahl_skater_summary_rates JOIN ahl_skater_summary ON ahl_skater_summary_rates.\"PLAYER\" = ahl_skater_summary.\"PLAYER\" AND ahl_skater_summary_rates.\"SEASON\" = ahl_skater_summary.\"SEASON\" JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND ahl_skater_summary.\"GP\" >= %s AND ahl_skater_summary.\"AGE\" > %s AND ahl_skater_summary.\"AGE\" < %s', [season.start_date, maxSeason.start_date, str(minGP), str(minAge), str(maxAge)])
		elif positions == 2:
			if report == 7:
				cursor.execute('SELECT * FROM ahl_skater_summary JOIN ahl_season ON ahl_skater_summary.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" <> %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
			elif report == 8:
				cursor.execute('SELECT * FROM ahl_skater_summary_rates JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" <> %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
			else:
				cursor.execute('SELECT ahl_skater_summary_rates.\"PLAYER\", ahl_skater_summary_rates.\"POS\", ahl_skater_summary_rates.\"AGE\", ahl_skater_summary_rates.\"SEASON\", ahl_skater_summary_rates.\"GP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"G/GP\") AS \"G\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A1/GP\") AS \"A1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A2/GP\") AS \"A2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A/GP\") AS \"A\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P/GP\") AS \"P\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P1/GP\") AS \"P1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"[+/-]/GP\") AS \"+/-\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PIM/GP\") AS \"PIM\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"S/GP\") AS \"S\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESG/GP\") AS \"ESG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA1/GP\") AS \"ESA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA2/GP\") AS \"ESA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA/GP\") AS \"ESA\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP/GP\") AS \"ESP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP1/GP\") AS \"ESP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPG/GP\") AS \"PPG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA1/GP\") AS \"PPA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA2/GP\") AS \"PPA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA/GP\") AS \"PPA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP/GP\") AS \"PPP\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP1/GP\") AS \"PPP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHG/GP\") AS \"SHG\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA1/GP\") AS \"SHA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHA2/GP\") AS \"SHA2\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA/GP\") AS \"SHA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHP/GP\") AS \"SHP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHP1/GP\") AS \"SHP1\" FROM ahl_skater_summary_rates JOIN ahl_skater_summary ON ahl_skater_summary_rates.\"PLAYER\" = ahl_skater_summary.\"PLAYER\" AND ahl_skater_summary_rates.\"SEASON\" = ahl_skater_summary.\"SEASON\" JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND ahl_skater_summary_rates.\"POS\" <> %s AND ahl_skater_summary.\"GP\" >= %s AND ahl_skater_summary.\"AGE\" > %s AND ahl_skater_summary.\"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
		elif positions == 3:
			if report == 7:
				cursor.execute('SELECT * FROM ahl_skater_summary JOIN ahl_season ON ahl_skater_summary.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
			elif report == 8:
				cursor.execute('SELECT * FROM ahl_skater_summary_rates JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
			else:
				cursor.execute('SELECT ahl_skater_summary_rates.\"PLAYER\", ahl_skater_summary_rates.\"POS\", ahl_skater_summary_rates.\"AGE\", ahl_skater_summary_rates.\"SEASON\", ahl_skater_summary_rates.\"GP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"G/GP\") AS \"G\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A1/GP\") AS \"A1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A2/GP\") AS \"A2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A/GP\") AS \"A\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P/GP\") AS \"P\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P1/GP\") AS \"P1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"[+/-]/GP\") AS \"+/-\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PIM/GP\") AS \"PIM\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"S/GP\") AS \"S\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESG/GP\") AS \"ESG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA1/GP\") AS \"ESA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA2/GP\") AS \"ESA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA/GP\") AS \"ESA\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP/GP\") AS \"ESP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP1/GP\") AS \"ESP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPG/GP\") AS \"PPG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA1/GP\") AS \"PPA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA2/GP\") AS \"PPA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA/GP\") AS \"PPA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP/GP\") AS \"PPP\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP1/GP\") AS \"PPP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHG/GP\") AS \"SHG\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA1/GP\") AS \"SHA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHA2/GP\") AS \"SHA2\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA/GP\") AS \"SHA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHP/GP\") AS \"SHP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHP1/GP\") AS \"SHP1\" FROM ahl_skater_summary_rates JOIN ahl_skater_summary ON ahl_skater_summary_rates.\"PLAYER\" = ahl_skater_summary.\"PLAYER\" AND ahl_skater_summary_rates.\"SEASON\" = ahl_skater_summary.\"SEASON\" JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND ahl_skater_summary_rates.\"POS\" = %s AND ahl_skater_summary.\"GP\" >= %s AND ahl_skater_summary.\"AGE\" > %s AND ahl_skater_summary.\"AGE\" < %s', [season.start_date, maxSeason.start_date, 'D', str(minGP), str(minAge), str(maxAge)])
		elif positions == 4:
			if report == 7:
				cursor.execute('SELECT * FROM ahl_skater_summary JOIN ahl_season ON ahl_skater_summary.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'C', str(minGP), str(minAge), str(maxAge)])
			elif report == 8:
				cursor.execute('SELECT * FROM ahl_skater_summary_rates JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'C', str(minGP), str(minAge), str(maxAge)])
			else:
				cursor.execute('SELECT ahl_skater_summary_rates.\"PLAYER\", ahl_skater_summary_rates.\"POS\", ahl_skater_summary_rates.\"AGE\", ahl_skater_summary_rates.\"SEASON\", ahl_skater_summary_rates.\"GP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"G/GP\") AS \"G\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A1/GP\") AS \"A1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A2/GP\") AS \"A2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A/GP\") AS \"A\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P/GP\") AS \"P\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P1/GP\") AS \"P1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"[+/-]/GP\") AS \"+/-\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PIM/GP\") AS \"PIM\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"S/GP\") AS \"S\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESG/GP\") AS \"ESG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA1/GP\") AS \"ESA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA2/GP\") AS \"ESA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA/GP\") AS \"ESA\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP/GP\") AS \"ESP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP1/GP\") AS \"ESP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPG/GP\") AS \"PPG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA1/GP\") AS \"PPA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA2/GP\") AS \"PPA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA/GP\") AS \"PPA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP/GP\") AS \"PPP\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP1/GP\") AS \"PPP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHG/GP\") AS \"SHG\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA1/GP\") AS \"SHA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHA2/GP\") AS \"SHA2\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA/GP\") AS \"SHA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHP/GP\") AS \"SHP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHP1/GP\") AS \"SHP1\" FROM ahl_skater_summary_rates JOIN ahl_skater_summary ON ahl_skater_summary_rates.\"PLAYER\" = ahl_skater_summary.\"PLAYER\" AND ahl_skater_summary_rates.\"SEASON\" = ahl_skater_summary.\"SEASON\" JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND ahl_skater_summary_rates.\"POS\" = %s AND ahl_skater_summary.\"GP\" >= %s AND ahl_skater_summary.\"AGE\" > %s AND ahl_skater_summary.\"AGE\" < %s', [season.start_date, maxSeason.start_date, 'C', str(minGP), str(minAge), str(maxAge)])
		elif positions == 5:
			if report == 7:
				cursor.execute('SELECT * FROM ahl_skater_summary JOIN ahl_season ON ahl_skater_summary.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', str(minGP), str(minAge), str(maxAge)])
			elif report == 8:
				cursor.execute('SELECT * FROM ahl_skater_summary_rates JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', str(minGP), str(minAge), str(maxAge)])
			else:
				cursor.execute('SELECT ahl_skater_summary_rates.\"PLAYER\", ahl_skater_summary_rates.\"POS\", ahl_skater_summary_rates.\"AGE\", ahl_skater_summary_rates.\"SEASON\", ahl_skater_summary_rates.\"GP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"G/GP\") AS \"G\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A1/GP\") AS \"A1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A2/GP\") AS \"A2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A/GP\") AS \"A\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P/GP\") AS \"P\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P1/GP\") AS \"P1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"[+/-]/GP\") AS \"+/-\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PIM/GP\") AS \"PIM\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"S/GP\") AS \"S\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESG/GP\") AS \"ESG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA1/GP\") AS \"ESA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA2/GP\") AS \"ESA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA/GP\") AS \"ESA\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP/GP\") AS \"ESP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP1/GP\") AS \"ESP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPG/GP\") AS \"PPG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA1/GP\") AS \"PPA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA2/GP\") AS \"PPA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA/GP\") AS \"PPA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP/GP\") AS \"PPP\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP1/GP\") AS \"PPP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHG/GP\") AS \"SHG\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA1/GP\") AS \"SHA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHA2/GP\") AS \"SHA2\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA/GP\") AS \"SHA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHP/GP\") AS \"SHP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHP1/GP\") AS \"SHP1\" FROM ahl_skater_summary_rates JOIN ahl_skater_summary ON ahl_skater_summary_rates.\"PLAYER\" = ahl_skater_summary.\"PLAYER\" AND ahl_skater_summary_rates.\"SEASON\" = ahl_skater_summary.\"SEASON\" JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND ahl_skater_summary_rates.\"POS\" = %s AND ahl_skater_summary.\"GP\" >= %s AND ahl_skater_summary.\"AGE\" > %s AND ahl_skater_summary.\"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', str(minGP), str(minAge), str(maxAge)])
		elif positions == 6:
			if report == 7:
				cursor.execute('SELECT * FROM ahl_skater_summary JOIN ahl_season ON ahl_skater_summary.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'RW', str(minGP), str(minAge), str(maxAge)])
			elif report == 8:
				cursor.execute('SELECT * FROM ahl_skater_summary_rates JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND \"POS\" = %s AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'RW', str(minGP), str(minAge), str(maxAge)])
			else:
				cursor.execute('SELECT ahl_skater_summary_rates.\"PLAYER\", ahl_skater_summary_rates.\"POS\", ahl_skater_summary_rates.\"AGE\", ahl_skater_summary_rates.\"SEASON\", ahl_skater_summary_rates.\"GP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"G/GP\") AS \"G\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A1/GP\") AS \"A1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A2/GP\") AS \"A2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A/GP\") AS \"A\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P/GP\") AS \"P\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P1/GP\") AS \"P1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"[+/-]/GP\") AS \"+/-\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PIM/GP\") AS \"PIM\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"S/GP\") AS \"S\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESG/GP\") AS \"ESG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA1/GP\") AS \"ESA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA2/GP\") AS \"ESA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA/GP\") AS \"ESA\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP/GP\") AS \"ESP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP1/GP\") AS \"ESP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPG/GP\") AS \"PPG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA1/GP\") AS \"PPA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA2/GP\") AS \"PPA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA/GP\") AS \"PPA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP/GP\") AS \"PPP\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP1/GP\") AS \"PPP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHG/GP\") AS \"SHG\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA1/GP\") AS \"SHA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHA2/GP\") AS \"SHA2\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA/GP\") AS \"SHA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHP/GP\") AS \"SHP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHP1/GP\") AS \"SHP1\" FROM ahl_skater_summary_rates JOIN ahl_skater_summary ON ahl_skater_summary_rates.\"PLAYER\" = ahl_skater_summary.\"PLAYER\" AND ahl_skater_summary_rates.\"SEASON\" = ahl_skater_summary.\"SEASON\" JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND ahl_skater_summary_rates.\"POS\" = %s AND ahl_skater_summary.\"GP\" >= %s AND ahl_skater_summary.\"AGE\" > %s AND ahl_skater_summary.\"AGE\" < %s', [season.start_date, maxSeason.start_date, 'RW', str(minGP), str(minAge), str(maxAge)])
		else:
			if report == 7:
				cursor.execute('SELECT * FROM ahl_skater_summary JOIN ahl_season ON ahl_skater_summary.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND (\"POS\" = %s OR \"POS\" = %s) AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', 'RW', str(minGP), str(minAge), str(maxAge)])
			elif report == 8:
				cursor.execute('SELECT * FROM ahl_skater_summary_rates JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND (\"POS\" = %s OR \"POS\" = %s) AND \"GP\" >= %s AND \"AGE\" > %s AND \"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', 'RW', str(minGP), str(minAge), str(maxAge)])
			else:
				cursor.execute('SELECT ahl_skater_summary_rates.\"PLAYER\", ahl_skater_summary_rates.\"POS\", ahl_skater_summary_rates.\"AGE\", ahl_skater_summary_rates.\"SEASON\", ahl_skater_summary_rates.\"GP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"G/GP\") AS \"G\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A1/GP\") AS \"A1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A2/GP\") AS \"A2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"A/GP\") AS \"A\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P/GP\") AS \"P\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"P1/GP\") AS \"P1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"[+/-]/GP\") AS \"+/-\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PIM/GP\") AS \"PIM\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"S/GP\") AS \"S\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESG/GP\") AS \"ESG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA1/GP\") AS \"ESA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA2/GP\") AS \"ESA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESA/GP\") AS \"ESA\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP/GP\") AS \"ESP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"ESP1/GP\") AS \"ESP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPG/GP\") AS \"PPG\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA1/GP\") AS \"PPA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA2/GP\") AS \"PPA2\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"PPA/GP\") AS \"PPA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP/GP\") AS \"PPP\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"PPP1/GP\") AS \"PPP1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHG/GP\") AS \"SHG\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA1/GP\") AS \"SHA1\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHA2/GP\") AS \"SHA2\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHA/GP\") AS \"SHA\", percent_rank()OVER (ORDER BY ahl_skater_summary_rates.\"SHP/GP\") AS \"SHP\", percent_rank() OVER (ORDER BY ahl_skater_summary_rates.\"SHP1/GP\") AS \"SHP1\" FROM ahl_skater_summary_rates JOIN ahl_skater_summary ON ahl_skater_summary_rates.\"PLAYER\" = ahl_skater_summary.\"PLAYER\" AND ahl_skater_summary_rates.\"SEASON\" = ahl_skater_summary.\"SEASON\" JOIN ahl_season ON ahl_skater_summary_rates.\"SEASON\" = ahl_season.name WHERE start_date >= %s AND start_date <= %s AND (ahl_skater_summary_rates.\"POS\" = %s OR ahl_skater_summary_rates.\"POS\" = %s) AND ahl_skater_summary.\"GP\" >= %s AND ahl_skater_summary.\"AGE\" > %s AND ahl_skater_summary.\"AGE\" < %s', [season.start_date, maxSeason.start_date, 'LW', 'RW', str(minGP), str(minAge), str(maxAge)])
		stats = cursor.fetchall()
		for s in stats:
			s = list(s)
			if report == 9:
				for i in range(5, 32):
					s[i] = round(s[i]*100, 1)
			result.append({'player':s[0], 'season':s[3][0:8], 'position':s[1], 'age':s[2], 'gp':s[4], 'g':s[5], 'a1':s[6], 'a2':s[7], 'a':s[8], 'p':s[9], 'p1':s[10], 'esg':s[14], 'esa1':s[15], 'esa2':s[16], 'esa':s[17], 'esp':s[18], 'esp1':s[19], 'ppg':s[20], 'ppa1':s[21], 'ppa2':s[22], 'ppa':s[23], 'ppp':s[24], 'ppp1':s[25], 'shg':s[26], 'sha1':s[27], 'sha2':s[28], 'sha':s[29], 'shp':s[30], 'shp1':s[31]})
	return result