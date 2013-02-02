/*
 * Instructions
 *
 *
 */


instructions = new Object();
instructions.challenge = "NONE";
instructions.waypoints = new Array();
instructions.boundaries = new Array();

$(function () {
  var mapWidget = new MapWidget();
  mapWidget.setMapCenter();
  mapWidget.add_marker();
  mapWidget.add_draggable();    
})

function senddata(){
	var postdata = JSON.stringify(instructions);
	var postArray = {json:postdata};
	
	
	var pathname = window.location.pathname;
	
	$.post('/api',postArray, function(data) {
	//do on success
	window.alert("Instructions sent");
	
	}); 
}

function addWaypoint(){
	var newWaypoint = new Array()
	newWaypoint [0] = 49.27628
	newWaypoint [1] = -123.17561
	newWaypoint [2] = "DEFAULT_TYPE"
	instructions.waypoints.push(newWaypoint) 
	
}

function addBoundary(){
	var newBoundary = new Array()
	newBoundary [0] = 49.27628
	newBoundary [1] = -123.17561
	newBoundary [2] = 10
	instructions.boundaries.push(newBoundary)
	
}

function setChallenge(sel){
	
	instructions.challenge = sel.options[sel.selectedIndex].value; 
}
