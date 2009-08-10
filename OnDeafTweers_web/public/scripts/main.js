$(document).ready(function() {
	$("#odt-form").submit(function() {
		$.get("/tweets/generate_report/" + $("#username").value, function(report) {});
	});
});

