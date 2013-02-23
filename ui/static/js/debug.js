
// The Debug Log is composed of human-readable log messages
function getDebugLog(){
    var pathname = window.location.pathname;
    
    $.ajax({
  		url: window.location.pathname + '/getlog',
  		type: 'GET',
  		dataType: "text",
  		success: function (data) {
        	$("#debugLogConsole").append(data+'<br/>');
        	// Make sure that we automatically scroll to the bottom 
        	$("#debugLogConsole").scrollTop($("#debugLogConsole")[0].scrollHeight);
        	console.log(data);
  		}
	});
}


// The position logs are composed of latitudes and longitudes
function getPositionLog(){

	    $.ajax({
        url: "/api?request=overviewData",
        type: 'GET',
        dataType: "json",
        success: function (overviewData) {
        	var positionString = overviewData.telemetry.longitude + ', ' + overviewData.telemetry.latitude;
        	$("#positionLogConsole").append(positionString +'<br/>');
        	// Make sure that we automatically scroll to the bottom 
        	$("#positionLogConsole").scrollTop($("#positionLogConsole")[0].scrollHeight);
        	console.log(positionString);
        	/*
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
	        
	     	mapWidget.update_boat_location(overviewData.telemetry.longitude, overviewData.telemetry.latitude);
	     	*/
    }
  });
}

// Call log updates every second
setInterval('getDebugLog()',1000);
setInterval('getPositionLog()',1000);