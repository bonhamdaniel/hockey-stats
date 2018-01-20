from django.urls import path
from . import views

app_name = 'timemachine'
urlpatterns = [
	# ex: /stats/
	path('', views.index, name='index'),
	# ex: /stats/team/
	path('team/', views.team, name='team'),
	# ex: /stats/player/
	path('players/', views.players, name='players'),
]