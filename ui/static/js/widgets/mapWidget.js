function MapWidget(listener){
    // Start position for the map (hardcoded here for simplicity)
    this.default_lat = 49.27628;
    this.default_lon = -123.17561;
    this.default_radius = 1000;
    this.zoom = 14;

    this.map; //complex object of type OpenLayers.Map
    this.boatLayer; //Layer for the boat marker
    this.waypointsLayer; // Layer for the waypoints of the the class
    this.boundariesLayer; // Layer for the boundaries of the class
    this.listener = listener || null;
  
    //Initialise the 'map' object
    map = new OpenLayers.Map("map", {
        controls: [
                    new OpenLayers.Control.Navigation(),
                    new OpenLayers.Control.ScaleLine({ geodesic: true }),
                    new OpenLayers.Control.MousePosition(), ],
        maxExtent: new OpenLayers.Bounds(-20037508.34, -20037508.34, 20037508.34, 20037508.34),
        maxResolution: 156543.0339,
        numZoomLevels: 19,
        units: 'm',
        projection: new OpenLayers.Projection("EPSG:900913"),
        displayProjection: new OpenLayers.Projection("EPSG:4326")
    });

    var tilesLayer = new OpenLayers.Layer.OSM("Local Tiles", "/static/tiles/${z}/${x}/${y}.png", { numZoomLevels: 19, alpha: true, isBaseLayer: true });
    map.addLayer(tilesLayer);

    //we create a new boat layer and add it to the map
    boatLayer = new OpenLayers.Layer.Markers("Boat");
    map.addLayer(boatLayer);
    
    //we create a new waypoints layer and add it to the map
    waypointsLayer = new OpenLayers.Layer.Markers("Waypoints");
    map.addLayer(waypointsLayer);
    
    //we create a new boundarys layer and add it to the map
    boundariesLayer = new OpenLayers.Layer.Vector("Boundaries");
    map.addLayer(boundariesLayer);
    
    
    // we add draggable control to the map
	var drag = new OpenLayers.Control.DragFeature(boundariesLayer, {onComplete: endDrag});
	map.addControl(drag);
	drag.activate();
	
	
	//we add feature selection control to the map
	var select = new OpenLayers.Control.SelectFeature(boundariesLayer, {	
																			hover: true});
	map.addControl(select);
	select.activate();
	
	//a function for handling the update information after the drag of a feature is done
	function endDrag(feature, pixel) {
	    var boundariesList = getBoundaries();
    	listener.updateBoundaries(boundariesList);
	}



	this.setMapCenter = function(lon,lat) {
	    lat = lat || this.default_lat;
	    lon = lon || this.default_lon;
        var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
        map.setCenter(lonLat, this.zoom);        
    }


    this.update_boat_location = function(lon,lat) {
    	try {
    		// When on the main page, the boatLayer isn't defined and therefore doesn't have functions such as addMarker()
    		// To avoid tons of error message, I have added this try/catch block
	        lat = lat || this.default_lat;
	        lon = lon || this.default_lon;
	        
	      	boatLayer.clearMarkers();
	
	        var size = new OpenLayers.Size(21, 25);
	        var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
	        var icon = new OpenLayers.Icon("static/img/map/boat-icon.png", size, offset);
	
	        var markerBoat = new OpenLayers.Marker(new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject()), icon);
	        boatLayer.addMarker(markerBoat);  
	     } catch (err) { }     
    }
    
 
    this.update_waypoints = function(waypoints_list) {        
                
        waypointsLayer.clearMarkers();
                
        var size = new OpenLayers.Size(21, 25);
       	var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
        var icon = new OpenLayers.Icon("static/img/map/marker.png", size, offset);
        
        for(var i=0; i<waypoints_list.length; i++){
          	var markerWaypoint = new OpenLayers.Marker(new OpenLayers.LonLat(waypoints_list[i][1], waypoints_list[i][0]).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject()), icon.clone());
        	waypointsLayer.addMarker(markerWaypoint);
        }                	      
    }
          
   	this.update_boundaries = function(boundaries_list){
    	
    	boundariesLayer.removeAllFeatures();
    	
    	for(var i=0; i<boundaries_list.length; i++){
    		var location = new OpenLayers.LonLat(boundaries_list[i][1], boundaries_list[i][0]).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
          	var point = new OpenLayers.Geometry.Point(location.lon, location.lat);
         	var boundary = OpenLayers.Geometry.Polygon.createRegularPolygon(point,boundaries_list[i][2],30,10);
          	var feature = new OpenLayers.Feature.Vector(boundary);
          	boundariesLayer.addFeatures([feature]);
        }
        
               
    }
    
    getBoundaries = function(){	
    	var boundaries = new Array();
    	for(var i=0; i<boundariesLayer.features.length; i++){
    		var newBoundary = new Array();
    		newBoundary [0] = boundariesLayer.features[i].geometry.getCentroid().transform(map.getProjectionObject(),new OpenLayers.Projection("EPSG:4326")).y;
  			newBoundary [1] = boundariesLayer.features[i].geometry.getCentroid().transform(map.getProjectionObject(),new OpenLayers.Projection("EPSG:4326")).x;
  			boundaries.push(newBoundary)
  		}
    	return boundaries;
    }
    
    
}
