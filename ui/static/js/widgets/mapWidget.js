function MapWidget(){
    // Start position for the map (hardcoded here for simplicity)
    this.default_lat = 49.27628;
    this.default_lon = -123.17561;
    this.zoom = 12;

    this.map; //complex object of type OpenLayers.Map

    this.vectors; //Layer for the vectors of the map
  
    this.boat; //Layer for the boat marker
    this.waypoints // Layer for the waypoints of the the class
    
    
    //this.draggablePointList; //A linkedList for storing the data of the draggable objects shown in the map.
    //this.draggableBoundaryList; //A linkedList for storing the data of the draggableBounday objects in the map.
    //this.markerPointList; //A linkedList for storing the data of the marker objects shown in the map.
    //this.markerBoundaryList; //A linkedList for storing the data of the markerBoundary objects in the map.

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

    // This is the layer that uses the locally stored tiles
    var newLayer = new OpenLayers.Layer.OSM("Local Tiles", "static/tiles/${z}/${x}/${y}.png", { numZoomLevels: 19, alpha: true, isBaseLayer: true });
    map.addLayer(newLayer);
    // This is the end of the layer


    //we create a new marker layer and add it to the map
    markers = new OpenLayers.Layer.Markers("Markers");
    map.addLayer(markers);

    // we create a new vector layer and add it to the map
    vectors = new OpenLayers.Layer.Vector("Vector Layer");
    map.addLayer(vectors);
    
    //we create a new boat layer and add it to the map
    boat = new OpenLayers.Layer.Markers("Boat");
    map.addLayer(boat);
    
    //we create a new waypoints layer and add it to the map
    waypoints = new OpenLayers.Layer.Markers("Waypoints");
    map.addLayer(waypoints);


    //It sets the center of the map to the coordinates specified by the Lon and Lat flot objects 
    //parameters: 
    //            map: the OpenLayes.Map object to which the OSM layer will be added. 
    //            lon: a float object describing the longitude of the center of the map
    //            Lat: a float object describing the latitude of the center of the map
    //            zoom: a integer object describing the zoom level to which the map will be set after this function is called
	this.setMapCenter = function(lon,lat) {
	    lat = lat || this.default_lat;
	    lon = lon || this.default_lon;
        var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
        map.setCenter(lonLat, this.zoom);        
    }


    //It adds a draggable feature to the map specified in the parameters
    //parameters: 
    //            vectors: the OpenLayers.Layer.Vector object to which the dragable feature will be added
    //            lon: a float object describing the longitude of the location of the draggable feature
    //            Lat: a float object describing the latitude of the location of the draggable feature
    //            map: the OpenLayes.Map object to which the draggable feature will be added.
    this.add_draggable = function(lon,lat) {
        lat = lat || this.default_lat;
        lon = lon || this.default_lon;

        var message = "lon:" + lon + ", lat:" + lat;      
                
        var location = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
        var point = new OpenLayers.Geometry.Point(location.lon, location.lat);
        vectors.addFeatures([new OpenLayers.Feature.Vector(point)]);
        var drag = new OpenLayers.Control.DragFeature(vectors, {
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
        
        boat.clearMarkers();
        
        var size = new OpenLayers.Size(21, 25);
        var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
        var icon = new OpenLayers.Icon("static/img/map/boat-icon.png", size, offset);

        var markerBoat = new OpenLayers.Marker(new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject()), icon);
        boat.addMarker(markerBoat);       
    }
    
    
    this.update_waypoints = function(waypoints_list) {
                
        waypoints.clearMarkers();
                
        var size = new OpenLayers.Size(21, 25);
       	var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
        var icon = new OpenLayers.Icon("static/img/map/marker.png", size, offset);
        
        for(var i=0; i<waypoints_list.length; i++){
          	var waypoint = new OpenLayers.Marker(new OpenLayers.LonLat(waypoints_list[i][1], waypoints_list[i][0]).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject()), icon);
        	waypoints.addMarker(waypoint);
        } 
               	      
    }	
    

}
