
//create map widget
$(function () {
  var mapWidget = new MapWidget();
  mapWidget.setMapCenter();
  mapWidget.add_marker();
  mapWidget.add_draggable();    
  mapWidget.add_marker(-70.66955, 42.59941);
  mapWidget.add_draggable(-70.66955, 42.59941);  
  mapWidget.pdate_boat_location(-70.67955, 42.48941);
})

  setInterval('getlog()',1000);

function getlog(){
    
    $.ajax({
  		url: window.location.pathname + "api?request=overviewData",
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
	        
	      	//update the map with some code here
  		}
	});

}


