/**
 * 
 */
 $('#statoptions').ready(function() {
	var league = $('#league').val();
	$.ajax({
		url: '/stats/ajax/getseasons/',
		data: {
			'league': league
		},
		dataType: 'json',
		success: function (data) {
			$('#minSeason').empty();
			$('#maxSeason').empty();
			if (league == '1') {
				d = data['leagueSeasons']
				for(i in d){
					$('#minSeason').append('<option value=' + d[i]['season_id'] + '>' + d[i]['season_id'] + '</option>');
					$('#maxSeason').append('<option value=' + d[i]['season_id'] + '>' + d[i]['season_id'] + '</option>');
				}
			}
			else {
				d = data['leagueSeasons']
				for(i in d){
					$('#minSeason').append('<option value=' + d[i]['season_id'] + '>' + d[i]['name'] + '</option>');
					$('#maxSeason').append('<option value=' + d[i]['season_id'] + '>' + d[i]['name'] + '</option>');
				}
			}
		}
	})
});

$('#statoptions').ready(function() {
	$(document).on('change', '#league', (function() {
		var league = $('#league').val();
		$.ajax({
			url: '/stats/ajax/getseasons/',
			data: {
				'league': league
			},
			dataType: 'json',
			success: function (data) {
				$('#minSeason').empty();
				$('#maxSeason').empty();
				if (league == '1') {
					d = data['leagueSeasons']
					for(i in d){
						$('#minSeason').append('<option value=' + d[i]['season_id'] + '>' + d[i]['season_id'] + '</option>');
						$('#maxSeason').append('<option value=' + d[i]['season_id'] + '>' + d[i]['season_id'] + '</option>');
					}
				}
				else {
					d = data['leagueSeasons']
					for(i in d){
						$('#minSeason').append('<option value=' + d[i]['season_id'] + '>' + d[i]['name'] + '</option>');
						$('#maxSeason').append('<option value=' + d[i]['season_id'] + '>' + d[i]['name'] + '</option>');
					}
				}
			}
		})
	}));
});