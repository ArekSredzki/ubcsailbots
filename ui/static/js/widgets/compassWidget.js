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
var sailLine;
var windDirection;



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
          offset: [25, 100],
          rotation: 0
        });
		

        
       	var sailLine = new Kinetic.Line({
        	points:[0,-20,sailLength,-20],
        	stroke: 'navy',
        	strokeWidth: 5,
        	lineCap: 'round',
        	lineJoin: 'round'
      	});
      	
      	
      	boatGroup = new Kinetic.Group({
      		x: stage.getWidth()/2,
      		y: stage.getHeight()/2
      	});
      	
      	boatGroup.add(sailboat);
      	boatGroup.add(sailLine);
      	
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
      
      // We want the sail at the top
      sailLayer.moveToTop();
      layer.draw();
});


function setSheet(sheetPercent) {
	/* Right now we are going to assume that 100% sheet corresponds to 0 degree angle
	 * 0% sheet corresponds to a 90 degree angle
	 */
}

function setBoatHeading(degreeHeading) {
	boatGroup.transitionTo({
            rotation: Math.PI * degreeHeading / 180,
            duration:1
    });
}

function setWindDirection(degreeWindDirection) {
	windDirection = degreeWindDirection;
	windWedge.transitionTo({
            rotation: Math.PI * (-90-20+degreeWindDirection) / 180,
            duration:1
    });
}




