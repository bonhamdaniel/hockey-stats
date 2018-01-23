/**
 * 
 */

/*function formatTable(column) {
	$("#sort").val(column);
	$("#pageNum").val(1);
	$("#table").submit();
}

function loadGoalieTable() {
	$("#tableFrame").attr("src", "goalietable.html?baseSeason=20162017&targetSeason=20162017&sort=svpct&min=20");
}

function loadSkaterTable() {
	$("#tableFrame").attr("src", "skatertable.html?baseSeason=20162017&targetSeason=20162017&sort=pts&min=20");
}

function loadCompTable() {
	$("#tableFrame").attr("src", "comptable.html?baseSeason=20162017&player1=8478550&player2=8476453&sort=pts");
}

$('#tableFrame').ready(function() {
	var recordPerPage = 25;
	var totalRows = $('#count').val();
	var totalPages = Math.ceil(totalRows / recordPerPage);
	var $pages = $('<div id="pages"></div>');
	$('<span id="page">' + 'Page' + '&nbsp;</span>').appendTo($pages);
	for (i = 0; i < totalPages; i++) {
		$('<span class="clickable">' + (i + 1) + '&nbsp;</span>').appendTo($pages);
	}
    $($pages).appendTo('#stattable');
    var tr = $('table tbody tr:has(td)');
    $('#pages').find('span').hide();
    var nums = $('#pages span');
    var page = $('#pageNum').val();
    $(nums[0]).show();
    $(nums[1]).show();
    var nBegin = parseInt(page - 10, 10);
    //nEnd = parseInt(page + 10, 10);
    for (var i = nBegin; i <= nBegin+20; i++) {
    	$(nums[i]).show();
    }
    if (nBegin > 2) $(nums[1]).after($("<span>...&nbsp;</span>"));
    if (nBegin+20 < nums.length-2) $(nums[nums.length-1]).before($("<span>...&nbsp;</span>"));
    $(nums[nums.length-1]).show();

	$('span:contains(' + page + '&nbsp;)').attr('class', 'current');// adds focus to currently selected page number
    // Handles the table pagination
	$('.clickable').click(function(event) {// fired when the user clicks for a new page of the table
		var page = $(this).text();
		$('#pageNum').val(parseInt(page));
		$("#table").submit();
	});
});*/

$('#statoptions').ready(function() {
	$(document).on('change', '.league', (function() {
		var league = $('#league').val();
		console.log(league);
	}));
});