console.info('compassWidget.js loaded')

var boatLength = 200;
var boatWidth = 50;
var sailLength = (boatLength/2)*1.05;

var stage;
var boatGroup;
var boatLayer;
var sailLayer;
var windWedge;
var windLayer;
var sailboat;
var sailMast;
var windHeading = 0;
var boatHeading = 0;
var sheetPercentHeading = 100;



$(function() {
	
	stage = new Kinetic.Stage({
        container: 'compassCanvas',
        width: 500,
        height: 400
      });

	 circleLayer = new Kinetic.Layer();

      var circle = new Kinetic.Circle({
        x: stage.getWidth() / 2,
        y: stage.getHeight() / 2,
        radius: (boatLength/2)*1.1,
        fill: 'silver',
        stroke: 'black',
        strokeWidth: 1,
        opacity: 0.5
      	});

      // add the shape to the layer
      circleLayer.add(circle);

      boatLayer = new Kinetic.Layer();
      
      var angularSpeed = Math.PI / 2;
      
      var imageObj = new Image();
      imageObj.onload = function() {
        sailboat = new Kinetic.Image({
          image: imageObj,
          width: boatWidth,
          height: boatLength,
          offset: [boatWidth/2, boatLength/2],
          rotation: 0
        });
		

        
       	sailMast = new Kinetic.Line({
        	points:[0,0,0,sailLength],
        	stroke: 'navy',
        	strokeWidth: 5,
        	lineCap: 'round',
        	lineJoin: 'round',
        	offset: [0,0]
      	});
      	
      	
      	boatGroup = new Kinetic.Group({
      		x: stage.getWidth()/2,
      		y: stage.getHeight()/2
      	});
      	
      	boatGroup.add(sailboat);
      	boatGroup.add(sailMast);
      	
      	boatLayer.add(boatGroup)
		stage.add(boatLayer);       
        
      };
      imageObj.src = 'ui/static/img/svg/sailboat.png';
      
      windLayer = new Kinetic.Layer();
      
      windWedge = new Kinetic.Wedge({
        x: stage.getWidth() / 2,
        y: stage.getHeight() / 2,
        radius: 50,
        angleDeg: 40,
        fill: 'white',
        stroke: 'black',
        strokeWidth: 2,
        offset: [-130,-40],
        rotationDeg: -90-20
      });

      // add the shape to the layer
      windLayer.add(windWedge);

      stage.add(circleLayer);
      stage.add(windLayer);
});


function setSheet(sheetPercent) {
	/* Right now we are going to assume that 100% sheet corresponds to 0 degree angle
	 * 0% sheet corresponds to a 90 degree angle
	 */
	var sheetDegrees;
	// Store the value we received in our global variable
	sheetPercentHeading = sheetPercent;
	if (sheetPercent > 100)
		sheetPercent = 100;
	else if (sheetPercent < 0)
		sheetPercent = 0;
	sheetDegrees = 90*(1-0.01*sheetPercent);
	
	if((windHeading - boatHeading) > 0 && (windHeading - boatHeading) > 180)
		sheetDegrees = (-1)*sheetDegrees;
		
	sailMast.transitionTo({
            rotation: Math.PI * sheetDegrees / 180,
            duration:1
    });
}

function setBoatHeading(degreeHeading) {
	boatHeading = degreeHeading;
	boatGroup.transitionTo({
            rotation: Math.PI * degreeHeading / 180,
            duration:1
    });
    // Update sheet because the wind may have crossed the transom
    setSheet(sheetPercentHeading);
}

function setWindDirection(degreeWindDirection) {
	windHeading = degreeWindDirection;
	windWedge.transitionTo({
            rotation: Math.PI * (-90-20+degreeWindDirection) / 180,
            duration:1
    });
    // Update sheet because the wind may have crossed the transom
    setSheet(sheetPercentHeading);
}




