"use strict";
var mapWidget;
var compassWidget;
var instructionsDataLocal;
//create map widget
$(function () {
  mapWidget = new MapWidget();
  setMapCenter();  
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
        timeout: 3000,
        success: function (overviewData) {
          console.log(overviewData);
	        $("#telemetry-speedOverGroundCell").text(overviewData.telemetry.SOG.toFixed(parseInt(2))+" m/s");
	        $("#telemetry-windDirectionCell").text(overviewData.telemetry.AWA.toFixed(parseInt(0))+ " degrees");
	        $("#telemetry-latitudeCell").text(overviewData.telemetry.latitude.toFixed(parseInt(5)));
	        $("#telemetry-longitudeCell").text(overviewData.telemetry.longitude.toFixed(parseInt(5)));
	        $("#connectionStatus-satNumCell").text(overviewData.connectionStatus.gpsSat);
	        if (overviewData.connectionStatus.automode == 1){
	          $("#connectionStatus-autoMode").text("Auto");
	        }
	        else{
            	$("#connectionStatus-autoMode").text("RC");
         	}
	        $("#connectionStatus-gpsAccuracyCell").text(overviewData.connectionStatus.HDOP);
	        $("#telemetry-rudderCell").text(overviewData.telemetry.Rudder);
	        if(overviewData.currentProcess.name == null){	        	
	        	$("#currentProcess-currentTaskCell").text("none");
	        }
	        else{
	        	$("#currentProcess-currentTaskCell").text(overviewData.currentProcess.name);
	        }
	        var timeInSeconds = overviewData.currentProcess.Starttime;
	        if(timeInSeconds != null){
		        var date = new Date(null);
		        date.setHours(0);
		        date.setSeconds(timeInSeconds);
		       	var time = date.toTimeString().substr(0,8);
		      	$("#currentProcess-elapsedTimeCell").text(time);
		 	    }
	        // Update map widget
	     	mapWidget.update_boat_location(overviewData.telemetry.longitude, overviewData.telemetry.latitude);
	     	
	     	// Update compass widget
	     	compassWidget.setSheet(overviewData.telemetry.SheetPercent);
	     	compassWidget.setBoatHeading(overviewData.telemetry.Heading);
	     	compassWidget.setWindDirection(overviewData.telemetry.AWA);
	     	setTimeout('getlog()',1000);
	      },
	      error: function(){
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
          console.log(instructionsData)
       		instructionsDataLocal = instructionsData;
          console.log(instructionsDataLocal);
    			mapWidget.update_waypoints(instructionsData.waypoints);
    			mapWidget.update_boundaries(instructionsData.boundaries);
	      }
	});
}

function setMapCenter(){
$.ajax({
        url: "api?request=overviewData",
        type: 'GET',
        dataType: "json",
        success: function (overviewData) {
          console.log(overviewData);
          mapWidget.setMapCenter(overviewData.telemetry.longitude, overviewData.telemetry.latitude);
        },
  });

}



