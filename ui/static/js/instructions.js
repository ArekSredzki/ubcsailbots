/*
 * Instructions
 *
 *
 */
var mapWidget;

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

$(function () {
  mapWidget = new MapWidget();
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

setInterval('getlog()',1000);

function getlog(){
    var telemetryData = new Array();
    
    $.get("api?request=overviewData",function(data){
        var overviewData = jQuery.parseJSON(data)
        console.log(overviewData);
        
        telemetryData[0] = overviewData.telemetry.latitude;
   		telemetryData[1] = overviewData.telemetry.longitude;
		
		mapWidget.update_boat_location(overviewData.telemetry.longitude, overviewData.telemetry.latitude);
	  }
	);
}





























