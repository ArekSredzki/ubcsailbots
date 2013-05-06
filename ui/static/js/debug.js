"use strict";
function logMessage(message, containerId)
{
	$(containerId).append(message + '<br />');
	$(containerId).scrollTop($(containerId)[0].scrollHeight);
}

// The Debug Log is composed of human-readable log messages
function getDebugLog(){
    var pathname = window.location.pathname;
    
    $.ajax({
  		url: window.location.pathname + '/getlog',
  		type: 'GET',
  		dataType: "text",
  		timeout: 3000,
  		success: function (data) {
  		  if (data!=""){
  			 logMessage(data, '#debugLogConsole');
  			}
        	//$("#debugLogConsole").append(data+'<br/>');
        	// Make sure that we automatically scroll to the bottom 
         setTimeout('getDebugLog()',1000);
      },
      error: function(){
          setTimeout('getDebugLog()',1000);
      }
	});
}


// Call log updates every second
setTimeout('getDebugLog()',1000);
