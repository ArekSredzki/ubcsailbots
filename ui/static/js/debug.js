
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
        	setTimeout('getDebugLog()',1000);

  		},
  		fail : function(){
  		  setTimeout('getDebugLog()',1000);
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
          setTimeout('getPositionLog()',1000);

        },
        fail : function(){
          setTimeout('getPositionLog()',1000);
        }
  });
}

// Call log updates every second
setTimeout('getDebugLog()',1000);
setTimeout('getPositionLog()',1000);