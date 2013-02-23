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
	updateWaypointDataDisplayTable()
}

function addBoundary(){
	var newBoundary = new Array()
	newBoundary [0] = overviewData.telemetry.latitude
	newBoundary [1] = overviewData.telemetry.longitude
	newBoundary [2] = 10
	instructions.boundaries.push(newBoundary)
	updateBoundaryDataDisplayTable()
}

function setChallenge(sel){
	
	instructions.challenge = sel.options[sel.selectedIndex].value; 
}
function updateWaypointDataDisplayTable(){
	var latTextBoxes = new Array("lat1", "lat2", "lat3", "lat4")
	var lonTextBoxes = new Array("lon1", "lon2", "lon3", "lon4")
	
	for(var i=0; i<instructions.waypoints.length; i++){
		$('#'+latTextBoxes[i]).val(instructions.waypoints[i][0])
		$('#'+lonTextBoxes[i]).val(instructions.waypoints[i][1])
	}
	
	
}
function updateBoundaryDataDisplayTable(){
	var latTextBoxes = new Array("lat1", "lat2")
	var lonTextBoxes = new Array("lon1", "lon2")
	var radTextBoxes = new Array("rad1", "rad2")
	
	for(var i=0; i<instructions.waypoints.length; i++){
		$('#'+latTextBoxes[i]).val(instructions.boundaries[i][0])
		$('#'+lonTextBoxes[i]).val(instructions.boundaries[i][1])
		$('#'+radTextBoxes[i]).val(instructions.boundaries[i][2])
	}
	
	
	
}

