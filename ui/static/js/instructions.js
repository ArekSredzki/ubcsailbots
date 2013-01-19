/*
 * Instructions
 *
 *
 */


instructions = new Object();
instructions.challenge = "NONE";
waypoint = new Array();
latitude = "+49.0000";
waypoint[0] = latitude;
longitude = "-123.0000";
waypoint[1] = longitude;
type = "GO_TO";
waypoint[2] = type;
instructions.waypoints = new Array();
instructions.waypoints.push(waypoint);

function senddata(){
	var postdata = JSON.stringify(instructions);
	var postArray = {json:postdata};
	
	
	var pathname = window.location.pathname;
	
	$.post('/api',postArray, function(data) {
	//do on success
	window.alert("Instructions sent");
	
	}); 
}