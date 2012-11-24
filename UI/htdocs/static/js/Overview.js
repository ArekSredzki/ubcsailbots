//create map widget
$(function () {
  initMapWidget();
  setMapCenter();
  var marker = add_marker();
  add_draggable();    
})

  setInterval('getlog()',1000);

function getlog(){
    var pathname = window.location.pathname;
    $.get(pathname + "api?request=overviewData",function(data){
        var overviewData = jQuery.parseJSON(data)
        console.log(overviewData);
        $("#connectionStatus-onlineOfflineCell").text(overviewData.connectionStatus.onlineOffline)
        $("#connectionStatus-batteryLevelCell").text(overviewData.connectionStatus.batteryLevel)
        $("#connectionStatus-satNumberCell").text(overviewData.connectionStatus.satNumber)
        $("#connectionStatus-gpsAccuracyCell").text(overviewData.connectionStatus.gpsAccuracy)
        $("#connectionStatus-hardwareHealthCell").text(overviewData.connectionStatus.hardwareHealth)
        $("#telemetry-speedOverGroundCell").text(overviewData.telemetry.speedOverGround)
        $("#telemetry-windDirectionCell").text(overviewData.telemetry.windDirection)
        $("#telemetry-currentManeuverCell").text(overviewData.telemetry.currentManeuver)
        $("#currentProcess-currentTaskCell").text(overviewData.currentProcess.task)
        $("#currentProcess-timeRemainingCell").text(overviewData.currentProcess.timeRemaining)
        $("#currentProcess-timeToCompletionCell").text(overviewData.currentProcess.timeToCompletion)
      ///update the map with some code here
    }
  );
}


