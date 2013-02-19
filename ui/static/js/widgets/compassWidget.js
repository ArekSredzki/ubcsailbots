console.info('compassWidget.js loaded')


$(function() {
	
	var stage = new Kinetic.Stage({
        container: 'compassCanvas',
        width: 500,
        height: 350
      });

      var layer = new Kinetic.Layer();
      
      var angularSpeed = Math.PI / 2;
      
      var imageObj = new Image();
      imageObj.onload = function() {
        var sailboat = new Kinetic.Image({
          x: stage.getWidth()/2,
          y: stage.getHeight()/2,
          image: imageObj,
          width: 50,
          height: 200,
          offset: [25, 100],
          rotation: 0
        });
		
        // add the shape to the layer
        layer.add(sailboat);

        // add the layer to the stage
        stage.add(layer);
        
        var anim = new Kinetic.Animation(function(frame) {
    			var angleDiff = frame.timeDiff * angularSpeed / 1000;
                sailboat.rotateDeg(angleDiff*10);
  		}, layer);
  		anim.start();
      };
      imageObj.src = 'ui/static/img/svg/sailboat.png';
});

function drawBoat(stage, layer) {
    var boatWidth = 40;
    var boatLength= 175; 
    var bowRadius = boatWidth/2;
    var boatStrokeWidth = 3;
    var sailLength = boatLength*0.7;
    
    
}

function drawSailRig(canvasWidth, canvasHeight, boomAngle) {
}



