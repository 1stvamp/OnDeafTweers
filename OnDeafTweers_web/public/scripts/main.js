$(function() {
	$("form").submit(function() {
		$.getJSON(
			"/tweets/report",
			{ username: $("username").value },
			function(data){
			}
		);
	});
});
