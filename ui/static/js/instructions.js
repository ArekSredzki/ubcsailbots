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
  $( "#description" ).combobox();

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
    	    console.log(overviewData)
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
	newWaypoint [0] = overviewData.telemetry.latitude
	newWaypoint [1] = overviewData.telemetry.longitude
	newWaypoint [2] = "pointToPoint"
	instructions.waypoints.push(newWaypoint) 
	mapWidget.update_waypoints(instructions.waypoints);
	updateWaypointDataDisplayTable()
	console.log(instructions.waypoints)
}

function addBoundary(){
	var newBoundary = new Array()
	newBoundary [0] = overviewData.telemetry.latitude
	newBoundary [1] = overviewData.telemetry.longitude
	newBoundary [2] = 50 //radius
	instructions.boundaries.push(newBoundary)
	mapWidget.update_boundaries(instructions.boundaries);
	updateBoundaryDataDisplayTable()
	console.log(instructions.boundaries)
}

function setChallenge(sel){
	instructions.challenge = sel.options[sel.selectedIndex].value;
	console.log(instructions.challenge) 
}
function updateWaypointDataDisplayTable(){
	var latTextBoxes = new Array("lat1", "lat2", "lat3", "lat4")
	var lonTextBoxes = new Array("lon1", "lon2", "lon3", "lon4")
	
	for(var i=0; i < 4 ; i++){
		$('#'+latTextBoxes[i]).val("")
		$('#'+lonTextBoxes[i]).val("")
	}
	for(var i=0; i<instructions.waypoints.length; i++){
		$('#'+latTextBoxes[i]).val(instructions.waypoints[i][0])
		$('#'+lonTextBoxes[i]).val(instructions.waypoints[i][1])
	}
	
	
}
function updateBoundaryDataDisplayTable(){
	var latTextBoxes = new Array("blat1", "blat2")
	var lonTextBoxes = new Array("blon1", "blon2")
	var radTextBoxes = new Array("brad1", "brad2")
	for(var i=0; i< 2; i++){
		$('#'+latTextBoxes[i]).val("")
		$('#'+lonTextBoxes[i]).val("")
		$('#'+radTextBoxes[i]).val("")
	}
	
	for(var i=0; i<instructions.boundaries.length; i++){
		$('#'+latTextBoxes[i]).val(instructions.boundaries[i][0])
		$('#'+lonTextBoxes[i]).val(instructions.boundaries[i][1])
		$('#'+radTextBoxes[i]).val(instructions.boundaries[i][2])
	}
	
	
	
}

function deleteWaypoint(index){
	instructions.waypoints.splice(index,1);
	mapWidget.update_waypoints(instructions.waypoints);
	updateWaypointDataDisplayTable();
}

function deleteBoundary(index){
	instructions.boundaries.splice(index,1);
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
