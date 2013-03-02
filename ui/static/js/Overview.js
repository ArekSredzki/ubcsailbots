var mapWidget;
var compassWidget;
var instructionsDataLocal;
//create map widget
$(function () {
  mapWidget = new MapWidget();
  mapWidget.setMapCenter();
  
  compassWidget = new CompassWidget();
  compassWidget.init();
  getInstructions();
})

setTimeout('getlog()',1000);

function getlog(){

	    $.ajax({
        url: "api?request=overviewData",
        type: 'GET',
        dataType: "json",
        success: function (overviewData) {
        	console.log(overviewData);
	        $("#connectionStatus-onlineOfflineCell").text(overviewData.connectionStatus.onlineOffline)
	        $("#connectionStatus-batteryLevelCell").text(overviewData.connectionStatus.batteryLevel)
	        $("#connectionStatus-satNumCell").text(overviewData.connectionStatus.gpsSatelliteNumber)
	        $("#connectionStatus-gpsAccuracyCell").text(overviewData.connectionStatus.gpsAccuracy)
	        $("#connectionStatus-hardwareHealthCell").text(overviewData.connectionStatus.hardwareHealth)
	        $("#telemetry-speedOverGroundCell").text(overviewData.telemetry.speedOverGround)
	        $("#telemetry-windDirectionCell").text(overviewData.telemetry.windDirection)
	        $("#telemetry-currentManeuverCell").text(overviewData.telemetry.currentManeuver)
	        $("#telemetry-latitudeCell").text(overviewData.telemetry.latitude)
	        $("#telemetry-longitudeCell").text(overviewData.telemetry.longitude)
	        $("#currentProcess-currentTaskCell").text(overviewData.currentProcess.task)
	        $("#currentProcess-timeRemainingCell").text(overviewData.currentProcess.timeRemaining)
	        $("#currentProcess-timeToCompletionCell").text(overviewData.currentProcess.timeToCompletion)
	        
	        // Update map widget
	     	mapWidget.update_boat_location(overviewData.telemetry.longitude, overviewData.telemetry.latitude);
	     	
	     	// Update compass widget
	     	compassWidget.setSheet(overviewData.telemetry.sailSheet)
	     	compassWidget.setBoatHeading(overviewData.telemetry.boatHeading)
	     	compassWidget.setWindDirection(overviewData.telemetry.windDirection)
	     	setTimeout('getlog()',1000);
      },
      fail: function(){
        setTimeout('getlog()',1000);
      }
  });

}

function getInstructions(){
	$.ajax({
        url: "api?request=instructionsData",
        type: 'GET',
        dataType: "json",
        success: function (instructionsData) {
     		instructionsDataLocal = instructionsData;
       		console.log(instructionsDataLocal);
  			mapWidget.update_waypoints(instructionsData.waypoints);
  			mapWidget.update_boundaries(instructionsData.boundaries);
	
		}
	});
}



