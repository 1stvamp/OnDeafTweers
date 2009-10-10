$(function() {
	$("form").submit(function() {
		$.getJSON(
			"/tweets/generate_report/" + $("#username").val(),
			{},
			function(report){
				report_element = $("#report");
				report_element.empty();
				for(i=0; i < report.length; i++) {
					row = report[i];
					if (row.mentioned || row.to) {
						li = document.createElement('li');
						li.html('User: ' + row.screen_name + ' (' + row.mentioned + ' ,' + row.to + ')');
						$('#report').append(li);
					} else {
						console.log('skipping');
					}
				}
				report_element.slideDown();
			}
		);
		return false;
	});
});
