/*
 * Instructions
 *
 *
 */
var mapWidget;
var overviewData;

instructions = new Object();
instructions.challenge = "NONE";
instructions.waypoints = new Array();
instructions.boundaries = new Array();
var mapWidget;

$(function () {
  mapWidget = new MapWidget(new MapListener());
  mapWidget.setMapCenter();
  mapWidget.setDraggableMode(true);
  setTimeout('getlog()',1000);
  
  	// install jquery ui elements
  	$('#sendDataButton').button();
  	$('#addWaypointButton').button();
  	$('#addBoundaryButton').button();
  	//$( "#description" ).combobox();
})


function getlog(){
    
    $.ajax({
        url: "api?request=overviewData",
        type: 'GET',
        dataType: "json",
        success: function (data) {
        	overviewData=data;
    			mapWidget.update_boat_location(overviewData.telemetry.longitude, overviewData.telemetry.latitude);
    	    setTimeout('getlog()',1000);
    	    console.log(overviewData);
	     },
	     fail : function(){
	       setTimeout('getlog()',1000);
	     }
	});
}

function senddata(){
	var postdata = JSON.stringify(instructions);
	console.log(instructions);
	
	var pathname = window.location.pathname;
	
	$.post('/api',postdata, function(data) {
		//do on success
		window.alert("Instructions sent and received: " + data);
	
	}); 
}


function addWaypoint(){
	var newWaypoint = new Array()
	newWaypoint [0] = overviewData.telemetry.latitude;
	newWaypoint [1] = overviewData.telemetry.longitude;
	newWaypoint [2] = "pointToPoint";
	
	
	instructions.waypoints.push(newWaypoint); 
	mapWidget.update_waypoints(instructions.waypoints);
	updateWaypointDataDisplayTable()
	console.log(instructions.waypoints)
	
}

function addBoundary(){
	var newBoundary = new Array();
	newBoundary [0] = overviewData.telemetry.latitude;
	newBoundary [1] = overviewData.telemetry.longitude;
	newBoundary [2] = 200 //radius
	instructions.boundaries.push(newBoundary);
	mapWidget.update_boundaries(instructions.boundaries);
	updateBoundaryDataDisplayTable();
	console.log(instructions.boundaries);
}

function setChallenge(sel){
	instructions.challenge = sel.options[sel.selectedIndex].value;
	console.log(instructions.challenge) ;
}

function updateWaypointDataDisplayTable()
{
	// First remove all rows from table
	$("#waypointListTable .waypointRow").remove();
	
	// Create waypoint template in a string
	var waypointRowString = 
	'<tr id="waypointRow$NUM" class="waypointRow"><td style="background:#5f9be3;color:#fff;">Wpt $NUM</td><td>lat:</td>' +
					'<td><input type="text" id="lat$NUM" size="8" onkeyup="updateWaypoints($NUM)"></td>' +
	        		'<td>lon:</td>' +
	        		'<td><input type="text" id="lon$NUM" size="8" onkeyup="updateWaypoints($NUM)"></td>' +
	        		'<td>type:</td>' +
	        		'<td><select id="waypointtype$NUM" onchange="updateWaypoints($NUM)"><option value="none"></option><option value="pointToPoint">Point to Point</option><option value="roundBuoyPort">Round BuoyPort</option><option value="roundBuoyStbd">Round Buoy Stbd</option><option value="ld_start_finish">ld Start Finish</option><option value="ld_first">ld First</option><option value="ld_second">ld Second</option><option value="nav_first">nav First</option><option value="nav_start_port">nav start port</option><option value="nav_start_stbd">nav start stb</option><option value="station_keeping">Station Keeping</option></select></td>' +
	        		'<td><button id="deleteWaypointButton$NUM" onclick="deleteWaypoint($NUM)">X</button></td>' +
	 '</tr>';
	 console.log(waypointRowString);
	
	// Foreach value in the length (including if there is no values), add a waypoint marker
	for (var i=0; i<instructions.waypoints.length; i++)
	{
		
		$('#waypointListTable > tbody:last').append(waypointRowString.split('$NUM').join(i+1));
		console.log('Added row to data display table');
		
		$('#lat'+(i+1)).val("");
		$('#lon'+(i+1)).val("");
		$('#waypointtype'+(i+1)).val("none");
	}
	
	for (var i=0; i<instructions.waypoints.length; i++){
		$('#lat'+(i+1)).val(instructions.waypoints[i][0]);
		$('#lon'+(i+1)).val(instructions.waypoints[i][1]);
		$('#waypointtype'+(i+1)).val(instructions.waypoints[i][2]);
	}
}

function updateBoundaryDataDisplayTable(){
		// First remove all rows from table
	$("#boundaryListTable .boundaryRow").remove();
	
	// Create waypoint template in a string
	var boundaryRowString = 
	'<tr id="boundaryRow$NUM" class="boundaryRow"><td style="background:#5f9be3;color:#fff;">Boundary $NUM</td><td>lat:</td>' +
					'<td><input type="text" id="blat$NUM" size="8" onkeyup="updateBoundaries($NUM)"></td>' +
	        		'<td>lon:</td>' +
	        		'<td><input type="text" id="blon$NUM" size="8" onkeyup="updateBoundaries($NUM)"></td>' +
	        		'<td>radius:</td>' +
	        		'<td> <input type="text" id="brad$NUM" size="8" onkeyup="updateBoundaries($NUM)"></td>' +
	        		'<td><button id="deleteBoundaryButton$NUM" onclick="deleteBoundary($NUM)">X</button></td>' +
	 '</tr>';
	 console.log(boundaryRowString);
	
	// Foreach value in the length (including if there is no values), add a waypoint marker
	for (var i=0; i<instructions.boundaries.length; i++)
	{
		
		$('#boundaryListTable > tbody:last').append(boundaryRowString.split('$NUM').join(i+1));
		console.log('Added row to data display table');
		
		$('#blat'+(i+1)).val("");
		$('#blon'+(i+1)).val("");
		$('#brad'+(i+1)).val("none");
	}
	
	for (var i=0; i<instructions.boundaries.length; i++){
		$('#blat'+(i+1)).val(instructions.boundaries[i][0]);
		$('#blon'+(i+1)).val(instructions.boundaries[i][1]);
		$('#brad'+(i+1)).val(instructions.boundaries[i][2]);
	}
	
}
function updateWaypoints(number){
  var index = number-1;
	instructions.waypoints[index][0]=parseFloat($('#lat'+number).val(),10)
	instructions.waypoints[index][1]=parseFloat($('#lon'+number).val(),10)
	instructions.waypoints[index][2]=$('#waypointtype'+number).val()
	mapWidget.update_waypoints(instructions.waypoints)	
		
}
function updateBoundaries(number){
  var index = number-1;
	instructions.boundaries[index][0]=parseFloat($('#blat'+number).val(),10)
	instructions.boundaries[index][1]=parseFloat($('#blon'+number).val(),10)
	instructions.boundaries[index][2]=parseFloat($('#brad'+number).val(),10)
	mapWidget.update_boundaries(instructions.boundaries);
}

function deleteWaypoint(number){
	// NOTE: number is not an index (shifted by +1)
	instructions.waypoints.splice(number-1,1);
	mapWidget.update_waypoints(instructions.waypoints);
	updateWaypointDataDisplayTable();
	
	// Delete the table row
	//$('#waypointRow' + (index+1)).remove();
}

function deleteBoundary(number){
	// NOTE: number is not an index (shifted by +1)
	instructions.boundaries.splice(number-1,1);
	mapWidget.update_boundaries(instructions.boundaries);
	updateBoundaryDataDisplayTable();
}



function MapListener(){
  
 this.updateBoundaries = function(boundariesList){
  for (var i=0; i<boundariesList.length; i++){
    instructions.boundaries[i][0] = boundariesList[i][0];
    instructions.boundaries[i][1] = boundariesList[i][1];
    instructions.boundaries[i][2] = boundariesList[i][2];
  }
  updateBoundaryDataDisplayTable();
 }
 
 this.updateWaypoints = function(waypointsList){
 	for (var i=0; i<waypointsList.length; i++){
    	instructions.waypoints[i][0] = waypointsList[i][0];
    	instructions.waypoints[i][1] = waypointsList[i][1];
  	}
  	updateWaypointDataDisplayTable();   
 } 
}









/* The following is a JQuery UI custom implementation of a combobox
 * It is recommended that you add all other javascript above this line
 * as the code below is not very human-readable
 */

(function( $ ) {
    $.widget( "ui.combobox", {
      _create: function() {
        var input,
          that = this,
          wasOpen = false,
          select = this.element.hide(),
          selected = select.children( ":selected" ),
          value = selected.val() ? selected.text() : "",
          wrapper = this.wrapper = $( "<span>" )
            .addClass( "ui-combobox" )
            .insertAfter( select );
 
        function removeIfInvalid( element ) {
          var value = $( element ).val(),
            matcher = new RegExp( "^" + $.ui.autocomplete.escapeRegex( value ) + "$", "i" ),
            valid = false;
          select.children( "option" ).each(function() {
            if ( $( this ).text().match( matcher ) ) {
              this.selected = valid = true;
              return false;
            }
          });
 
          if ( !valid ) {
            // remove invalid value, as it didn't match anything
            $( element )
              .val( "" )
              .attr( "title", value + " didn't match any item" )
              .tooltip( "open" );
            select.val( "" );
            setTimeout(function() {
              input.tooltip( "close" ).attr( "title", "" );
            }, 2500 );
            input.data( "ui-autocomplete" ).term = "";
          }
        }
 
        input = $( "<input>" )
          .appendTo( wrapper )
          .val( value )
          .attr( "title", "" )
          .addClass( "ui-state-default ui-combobox-input" )
          .autocomplete({
            delay: 0,
            minLength: 0,
            source: function( request, response ) {
              var matcher = new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );
              response( select.children( "option" ).map(function() {
                var text = $( this ).text();
                if ( this.value && ( !request.term || matcher.test(text) ) )
                  return {
                    label: text.replace(
                      new RegExp(
                        "(?![^&;]+;)(?!<[^<>]*)(" +
                        $.ui.autocomplete.escapeRegex(request.term) +
                        ")(?![^<>]*>)(?![^&;]+;)", "gi"
                      ), "<strong>$1</strong>" ),
                    value: text,
                    option: this
                  };
              }) );
            },
            select: function( event, ui ) {
              ui.item.option.selected = true;
              that._trigger( "selected", event, {
                item: ui.item.option
              });
            },
            change: function( event, ui ) {
              if ( !ui.item ) {
                removeIfInvalid( this );
              }
            }
          })
          .addClass( "ui-widget ui-widget-content ui-corner-left" );
 
        input.data( "ui-autocomplete" )._renderItem = function( ul, item ) {
          return $( "<li>" )
            .append( "<a>" + item.label + "</a>" )
            .appendTo( ul );
        };
 
        $( "<a>" )
          .attr( "tabIndex", -1 )
          .attr( "title", "Show All Items" )
          .tooltip()
          .appendTo( wrapper )
          .button({
            icons: {
              primary: "ui-icon-triangle-1-s"
            },
            text: false
          })
          .removeClass( "ui-corner-all" )
          .addClass( "ui-corner-right ui-combobox-toggle" )
          .mousedown(function() {
            wasOpen = input.autocomplete( "widget" ).is( ":visible" );
          })
          .click(function() {
            input.focus();
 
            // close if already visible
            if ( wasOpen ) {
              return;
            }
 
            // pass empty string as value to search for, displaying all results
            input.autocomplete( "search", "" );
          });
 
        input.tooltip({
          tooltipClass: "ui-state-highlight"
        });
      },
 
      _destroy: function() {
        this.wrapper.remove();
        this.element.show();
      }
    });
  })( jQuery );
