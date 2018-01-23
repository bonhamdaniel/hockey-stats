from django.urls import path
from . import views

app_name = 'stats'
urlpatterns = [
	# ex: /stats/
	path('', views.index, name='index'),
	# ex: /stats/team/
	path('team/', views.team, name='team'),
	# ex: /stats/player/
	path('players/', views.players, name='players'),
	# ex: /stats/locations/
	path('locations/', views.locations, name='locations'),
	# Ajax to get seasons
	path('ajax/getseasons/', views.getSeasons, name='getseasons'),
	# Ajax to get skaters
	path('ajax/getskaters/', views.getSkaters, name='getskaters'),
]