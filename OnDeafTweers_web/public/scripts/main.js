$(function() {
	$("form").submit(function() {
		$.getJSON(
			"/tweets/report",
			{ username: $("#username").val() },
			function(report){
				report_element = $("#report");
				report_element.empty();
				report.each(function(i) {
					li = document.createElement('li');
				}
				report_element.slideDown();
			}
		);
		return false;
	});
});
