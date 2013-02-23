/*
 * Instructions
 *
 *
 */
var mapWidget;
var overviewData;

instructions = new Object();
instructions.challenge = "NONE";
instructions.waypoints = new Array();
instructions.boundaries = new Array();
var mapWidget;

$(function () {
  mapWidget = new MapWidget();
  mapWidget.setMapCenter();
  setInterval('getlog()',1000);
})


function getlog(){
    
    $.ajax({
        url: "api?request=overviewData",
        type: 'GET',
        dataType: "json",
        success: function (data) {
        	overviewData=data;
			mapWidget.update_boat_location(overviewData.telemetry.longitude, overviewData.telemetry.latitude);
	  }
	});
}

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
	newWaypoint [0] = overviewData.telemetry.latitude
	newWaypoint [1] = overviewData.telemetry.longitude
	newWaypoint [2] = "DEFAULT_TYPE"
	instructions.waypoints.push(newWaypoint) 
	mapWidget.update_waypoints(instructions.waypoints);
}

function addBoundary(){
	var newBoundary = new Array()
	newBoundary [0] = overviewData.telemetry.latitude
	newBoundary [1] = overviewData.telemetry.longitude
	newBoundary [2] = 50 //radius
	instructions.boundaries.push(newBoundary)
	mapWidget.update_boundaries(instructions.boundaries);
}

function setChallenge(sel){
	
	instructions.challenge = sel.options[sel.selectedIndex].value; 
}
