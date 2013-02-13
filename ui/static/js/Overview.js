var mapWidget;
//create map widget
$(function () {
  mapWidget = new MapWidget();
  mapWidget.setMapCenter();
  mapWidget.add_marker();
  mapWidget.add_boundary();
})

  setInterval('getlog()',1000);

function getlog(){
    var longitude;
    $.get("api?request=overviewData",function(data){
        var overviewData = jQuery.parseJSON(data)
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
        
     	mapWidget.update_boat_location(overviewData.telemetry.longitude, overviewData.telemetry.latitude);
    }
  );

}


