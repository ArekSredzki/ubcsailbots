console.info('compassWidget.js loaded')


$(function() {
    var canvas = $("#compassWidgetCanvas");
    var canvasWidth = canvas.width();
    var canvasHeight = canvas.height();    
    
    canvas.drawArc({
    	layer: true,
    	group: "HUD",
        fillStyle: "lightgray",
        shadowColor: "#5f9be3",
        shadowBlur: 30,
        x: canvasWidth/2, y: canvasHeight/2,
        radius: canvasWidth/4
    });
    
    drawBoat(canvas,0);
    
	$("canvas").animateLayerGroup("boat", {
	  //rotate: "+=180"
	});
});

function drawBoat(canvas, boatAngle, sailAngle) {
    var boatWidth = 40;
    var boatLength= 175; 
    var bowRadius = boatWidth/2;
    var boatStrokeWidth = 3;
    var sailLength = boatLength*0.7;
    // Draw main boat body
    canvas.drawRect({
        strokeStyle: "black",
        layer: true,
        group: "boat",
        strokeWidth: boatStrokeWidth,
        x: canvas.width()/2, y: canvas.height()/2,
        width: boatWidth,
        height: boatLength - bowRadius,
        cornerRadius: 2,
        rotate: boatAngle
    });
    // Draw boat bow
    canvas.drawArc({
      strokeStyle:"black",
      layer: true,
      group: "boat",
      strokeWidth: boatStrokeWidth,
      x: canvas.width()/2, y: canvas.height()/2-(boatLength-bowRadius)/2,
      radius: bowRadius,
      start: -90, end: 90,
      closed: false
    });
    
    
    // Draw Sail
    canvas.drawLine({
      strokeStyle: "black",
      layer: true,
      group: "boat",
      strokeWidth: boatStrokeWidth-1,
      x1: canvas.width()/2, y1: canvas.height()/2-30,
      x2: (canvas.width()/2)+sailLength-15, y2: (canvas.height())/2+40
    });
}

function drawSailRig(canvasWidth, canvasHeight, boomAngle) {
}

