from jchart import Chart
from .models import NhlTeam, NhlTeamSummary, AhlSeason, NhlShot, NhlPlayer
from django.db.models import Q
from django.db import connection

class BubbleChart(Chart):
	chart_type = 'bubble'
	options = {
		'maintainAspectRatio': True,
		'scaleShowGridLines': False
	}

	def get_datasets(self, leagueChoice, season1Choice, season2Choice, skaters, reportChoice):
		if season1Choice == season2Choice:
			sLabel = season1Choice + ' '
		else:
			sLabel = season1Choice + ' to ' + season2Choice + ' '
		pLabel = ' - ' + NhlPlayer.objects.get(pk=skaters).player_name
		with connection.cursor() as cursor:
			if int(reportChoice) == 1:
				cursor.execute('SELECT \"X\", \"Y\", Count(*) FROM nhl_locations_blocks_blockers WHERE season_id >= %s AND season_id <= %s AND blocker = %s GROUP BY \"X\", \"Y\"', [str(season1Choice), str(season2Choice), str(skaters)])
				rLabel = 'NHL Blocks '
			elif int(reportChoice) == 3:
				cursor.execute('SELECT \"X\", \"Y\", Count(*) FROM nhl_locations_giveaways_givers WHERE season_id >= %s AND season_id <= %s AND culprit = %s GROUP BY \"X\", \"Y\"', [str(season1Choice), str(season2Choice), str(skaters)])
				rLabel = 'NHL Giveaways '
			elif int(reportChoice) == 4:
				cursor.execute('SELECT \"X\", \"Y\", Count(*) FROM nhl_locations_goals_scorers WHERE season_id >= %s AND season_id <= %s AND scorer = %s GROUP BY \"X\", \"Y\"', [str(season1Choice), str(season2Choice), str(skaters)])
				rLabel = 'NHL Goals '
			elif int(reportChoice) == 5:
				cursor.execute('SELECT \"X\", \"Y\", Count(*) FROM nhl_locations_hits_hitters WHERE season_id >= %s AND season_id <= %s AND hitter = %s GROUP BY \"X\", \"Y\"', [str(season1Choice), str(season2Choice), str(skaters)])
				rLabel = 'NHL Hits '
			elif int(reportChoice) == 6:
				cursor.execute('SELECT \"X\", \"Y\", Count(*) FROM nhl_locations_penalties_takers WHERE season_id >= %s AND season_id <= %s AND taker = %s GROUP BY \"X\", \"Y\"', [str(season1Choice), str(season2Choice), str(skaters)])
				rLabel = 'NHL Penalties '
			elif int(reportChoice) == 7:
				cursor.execute('SELECT \"X\", \"Y\", Count(*) FROM nhl_locations_shots_shooters WHERE season_id >= %s AND season_id <= %s AND shooter = %s GROUP BY \"X\", \"Y\"', [str(season1Choice), str(season2Choice), str(skaters)])
				rLabel = 'NHL Shots '
			elif int(reportChoice) == 8:
				cursor.execute('SELECT \"X\", \"Y\", Count(*) FROM nhl_locations_takeaways_takers WHERE season_id >= %s AND season_id <= %s AND taker = %s GROUP BY \"X\", \"Y\"', [str(season1Choice), str(season2Choice), str(skaters)])
				rLabel = 'NHL Takeaways '

			results = cursor.fetchall()
			data = [{'x': data[0], 'y':data[1], 'r':data[2]*5} for data in results]
			return [{'label': rLabel + sLabel + pLabel,
					'data': data
					}]