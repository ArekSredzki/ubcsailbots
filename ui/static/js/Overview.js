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
	        $("#telemetry-speedOverGroundCell").text(overviewData.telemetry.SOG.toFixed(parseInt(2))+" m/s");
	        $("#telemetry-windDirectionCell").text(overviewData.telemetry.AWA.toFixed(parseInt(0))+ " degrees");
	        $("#telemetry-latitudeCell").text(overviewData.telemetry.latitude.toFixed(parseInt(5)));
	        $("#telemetry-longitudeCell").text(overviewData.telemetry.longitude.toFixed(parseInt(5)));
	        $("#telemetry-rudderCell").text(overviewData.telemetry.rudder);
	        
	        // Update map widget
	     	mapWidget.update_boat_location(overviewData.telemetry.longitude, overviewData.telemetry.latitude);
	     	
	     	// Update compass widget
	     	compassWidget.setSheet(overviewData.telemetry.SheetPercent);
	     	compassWidget.setBoatHeading(overviewData.telemetry.Heading);
	     	compassWidget.setWindDirection(overviewData.telemetry.AWA);
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
          console.log(instructionsData)
       		instructionsDataLocal = instructionsData;
          console.log(instructionsDataLocal);
    			mapWidget.update_waypoints(instructionsData.waypoints);
    			mapWidget.update_boundaries(instructionsData.boundaries);
	      }
	});
}



