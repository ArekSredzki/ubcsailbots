function MapWidget(){
    // Start position for the map (hardcoded here for simplicity)
    this.default_lat = 49.27628;
    this.default_lon = -123.17561;
    this.default_radius = 1000;
    this.zoom = 14;

    this.map; //complex object of type OpenLayers.Map
    this.vectorLayer; //Layer for the vectorLayer of the map  
    this.boatLayer; //Layer for the boat marker
    this.waypointsLayer; // Layer for the waypoints of the the class
  
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

    var tilesLayer = new OpenLayers.Layer.OSM("Local Tiles", "/ui/static/tiles/${z}/${x}/${y}.png", { numZoomLevels: 19, alpha: true, isBaseLayer: true });
    map.addLayer(tilesLayer);

    // we create a new vector layer and add it to the map
    vectorLayer = new OpenLayers.Layer.Vector("Boundaries");
    map.addLayer(vectorLayer);
    
    //we create a new boat layer and add it to the map
    boatLayer = new OpenLayers.Layer.Markers("Boat");
    map.addLayer(boatLayer);
    
    //we create a new waypoints layer and add it to the map
    waypointsLayer = new OpenLayers.Layer.Markers("Waypoints");
    map.addLayer(waypointsLayer);


	this.setMapCenter = function(lon,lat) {
	    lat = lat || this.default_lat;
	    lon = lon || this.default_lon;
        var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
        map.setCenter(lonLat, this.zoom);        
    }


 
    this.add_draggable = function(lon,lat) {
        lat = lat || this.default_lat;
        lon = lon || this.default_lon;

        var message = "lon:" + lon + ", lat:" + lat;      
                
        var location = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
        var point = new OpenLayers.Geometry.Point(location.lon, location.lat);
        vectorLayer.addFeatures([new OpenLayers.Feature.Vector(point)]);
        var drag = new OpenLayers.Control.DragFeature(vectorLayer, {
            autoActivate: true,
            onComplete: function () {                  //this function is called when the drag feature is released                 
                alert(message)
            }
        });
        map.addControl(drag);
        drag.activate();
    }

    this.update_boat_location = function(lon,lat) {
        lat = lat || this.default_lat;
        lon = lon || this.default_lon;
        
        boatLayer.clearMarkers();
        
        var size = new OpenLayers.Size(21, 25);
        var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
        var icon = new OpenLayers.Icon("static/img/map/boat-icon.png", size, offset);

        var markerBoat = new OpenLayers.Marker(new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject()), icon);
        boatLayer.addMarker(markerBoat);       
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
    
   this.add_boundary = function(lon,lat,radius){
    	lat = lat || this.default_lat;
    	lon = lon || this.default_lon;
    	radius = radius || this.default_radius;
    	var location = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
        var point = new OpenLayers.Geometry.Point(location.lon, location.lat);
    	var boundary = OpenLayers.Geometry.Polygon.createRegularPolygon(point,radius,30,10);
    	var feature = new OpenLayers.Feature.Vector(boundary);  
    	vectors.addFeatures([feature]);
    }
    
}
