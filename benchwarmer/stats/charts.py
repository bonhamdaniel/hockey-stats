from jchart import Chart
from .models import NhlTeam, NhlTeamSummary, AhlSeason, NhlShot
from django.db.models import Q
from django.db import connection

class BubbleChart(Chart):
	chart_type = 'bubble'
	options = {
		'maintainAspectRatio': True,
		'scaleShowGridLines': False
	}

	def get_datasets(self):
		with connection.cursor() as cursor:
			#shots = NhlShot.objects.filter(Q(game_id__gt=2017010000)&Q(x__gt=-200))
			cursor.execute('SELECT * FROM nhl_shot_location WHERE season_id = 20172018 AND "X" > 0 AND "X" < 100')
			shots = cursor.fetchall()
			data = [{'x': shot[2], 'y':shot[3]} for shot in shots]
			return [{'label': 'NHL Shot Location 2017-18',
					'data': data
					}]