// Start position for the map (hardcoded here for simplicity)
        var lat = 49.27628;
        var lon = -123.17561;
        var zoom = 12;

        var map; //complex object of type OpenLayers.Map

        //Initialise the 'map' object
        function init() {

            map = new OpenLayers.Map("map", {
                controls: [
                    new OpenLayers.Control.Navigation(),
                    new OpenLayers.Control.ScaleLine({ geodesic: true }),
                    new OpenLayers.Control.MousePosition(),],
                maxExtent: new OpenLayers.Bounds(-20037508.34, -20037508.34, 20037508.34, 20037508.34),
                maxResolution: 156543.0339,
                numZoomLevels: 19,
                units: 'm',
                projection: new OpenLayers.Projection("EPSG:900913"),
                displayProjection: new OpenLayers.Projection("EPSG:4326")
            });

			/*uncomment below to put in map from web*/			
//  			layerMapnik = new OpenLayers.Layer.OSM.Mapnik("Mapnik");
//  			layerMapnik.setOpacity(0.4);
//  			map.addLayer(layerMapnik);						
//  			var switcherControl = new OpenLayers.Control.LayerSwitcher();
//  			map.addControl(switcherControl);
//  			switcherControl.maximizeControl();

            // This is the layer that uses the locally stored tiles
            var newLayer = new OpenLayers.Layer.OSM("Local Tiles", "static/tiles/${z}/${x}/${y}.png", { numZoomLevels: 19, alpha: true, isBaseLayer: true });
            map.addLayer(newLayer);
            // This is the end of the layer


            if (!map.getCenter()) {
                var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
                map.setCenter(lonLat, zoom);
            }
                                 
            //now we call the add_marker function for adding a new marker_layer with the marker, we set it up to lon-lat for testing.
            add_marker(map, lon, lat)
        }


        //Adds a marker layer to the map and calls addMarker.        
        function add_marker(map, lon, lat) {
           
            //we create a new marker layer and add it to the map
            var markers = new OpenLayers.Layer.Markers("Markers");
            map.addLayer(markers);
            
            //here we define all the properties of the icon for the marker
            var size = new OpenLayers.Size(21, 25);
            var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
            var icon = new OpenLayers.Icon("static/img/map/marker.png", size, offset);

            markers.addMarker(new OpenLayers.Marker(new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject()), icon));                        
        }


    