function logMessage(message, logName, containerId)
{
	var now = new Date();
	var month=new Array();
	month[0]="January";
	month[1]="February";
	month[2]="March";
	month[3]="April";
	month[4]="May";
	month[5]="June";
	month[6]="July";
	month[7]="August";
	month[8]="September";
	month[9]="October";
	month[10]="November";
	month[11]="December";
	
   	var currentTime = now.getHours()+':'+now.getMinutes()+':'+now.getSeconds();
   	var currentFullDate = now.getFullYear() + ':' + month[now.getMonth()] + ':' + now.getDate() + ':' + now.getHours()+':'+now.getMinutes()+':'+now.getSeconds();



	$(containerId).append(currentTime + ', ' + message + '<br />');
	$(containerId).scrollTop($(containerId)[0].scrollHeight);
	
	console.log(currentFullDate + ', ' + message);
}



// The Debug Log is composed of human-readable log messages
function getDebugLog(){
    var pathname = window.location.pathname;
    
    $.ajax({
  		url: window.location.pathname + '/getlog',
  		type: 'GET',
  		dataType: "text",
  		success: function (data) {
  			logMessage(data, 'Debug Messages', '#debugLogConsole');
        	//$("#debugLogConsole").append(data+'<br/>');
        	// Make sure that we automatically scroll to the bottom 
        	//$("#debugLogConsole").scrollTop($("#debugLogConsole")[0].scrollHeight);
        	//console.log(data);
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
        	logMessage(positionString, 'Position Log', '#positionLogConsole');
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