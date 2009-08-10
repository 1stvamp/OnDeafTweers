function update_status() {
}
$(document).ready(function() {
	$("#odt-form").submit(function() {
		$.get("/tweets/generate_report/" + $("#username").val(), function(report) {
			report_element = $("#report");
			report_element.empty();
			report.each(function(i) {
				li = document.createElement('li');
			}
			report_element.slideDown();
		});
	});
});

