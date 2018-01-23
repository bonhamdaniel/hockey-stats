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
					$('#minSeason').val(d[0]['season_id'])
				}
				else {
					d = data['leagueSeasons']
					for(i in d){
						$('#minSeason').append('<option value=' + d[i]['season_id'] + '>' + d[i]['name'] + '</option>');
						$('#maxSeason').append('<option value=' + d[i]['season_id'] + '>' + d[i]['name'] + '</option>');
					}
					$('#minSeason').val(d[0]['season_id'])
				}
			}
		})
	}));
});

 $('#statoptions').ready(function() {
	var league = $('#league').val();
	var position = $('#position').val();
	var minSeason = $('#minSeason').val();
	var maxSeason = $('#maxSeason').val();
	$.ajax({
		url: '/stats/ajax/getskaters/',
		data: {
			'league': league,
			'position': position,
			'minSeason': minSeason,
			'maxSeason': maxSeason
		},
		dataType: 'json',
		success: function (data) {
			$('#skaters').empty();
			d = data['skaters']
			for(i in d){
				console.log(d[i][0])
				$('#skaters').append('<option value=' + d[i][0] + '>' + d[i][1] + '</option>');
			}
		}
	})
});

$('#statoptions').ready(function() {
	$(document).on('change', '#league', (function() {
		var league = $('#league').val();
		var position = $('#position').val();
		var minSeason = $('#minSeason').val();
		var maxSeason = $('#maxSeason').val();
		$.ajax({
			url: '/stats/ajax/getskaters/',
			data: {
				'league': league,
				'position': position,
				'minSeason': minSeason,
				'maxSeason': maxSeason
			},
			dataType: 'json',
			success: function (data) {
				$('#skaters').empty();
				d = data['skaters']
				for(i in d){
					$('#skaters').append('<option value=' + d[i][0] + '>' + d[i][1] + '</option>');
				}
				$('#skaters').val(d[0][0])
			}
		})
	}));

	$(document).on('change', '#position', (function() {
		var league = $('#league').val();
		var position = $('#position').val();
		var minSeason = $('#minSeason').val();
		var maxSeason = $('#maxSeason').val();
		$.ajax({
			url: '/stats/ajax/getskaters/',
			data: {
				'league': league,
				'position': position,
				'minSeason': minSeason,
				'maxSeason': maxSeason
			},
			dataType: 'json',
			success: function (data) {
				$('#skaters').empty();
				d = data['skaters']
				for(i in d){
					console.log(d[i][0])
					$('#skaters').append('<option value=' + d[i][0] + '>' + d[i][1] + '</option>');
				}
				$('#skaters').val(d[0][0])
			}
		})
	}));
});