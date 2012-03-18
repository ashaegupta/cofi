var map;
var GET_search = "/cofi/places?"
var places = [];
var maxPlaces = 15;

// Map current location
function initialize_current_location_on_map(lat, lon) {
    var options = {
      center: new google.maps.LatLng(lat, lon),
      zoom: 15,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("map_canvas"),
        options);
}

// A jsonp request script
function load_places_jspon_script(url) {
    /* makes a jsonp request for _src */
    var e = document.createElement('script');
    e.setAttribute('language','javascript'); 
    e.setAttribute('type', 'text/javascript');
    e.setAttribute('src', url); 
    var parent = document.head;
    parent.appendChild(e);
}

// Callback function for load_places_script. Also parses json response to return list of places
function handle_request(response) {
    console.log(response);
    places = response.data;
    console.log("handling request...");
    map_places(places);
}

// Map places
function map_places(places){
    for (i=0; i<places.length && i< maxPlaces; i++) {
        console.log("mapping places...");
        var lat = places[i].location.coordinate.latitude;
        var lon = places[i].location.coordinate.longitude;
        console.log(places[i].name);
        var loc = new google.maps.LatLng(lat,lon);
        add_marker(loc);
    }
    new adjust_map_bounds();
}

// Set marker characteristics
function add_marker(loc){
    console.log("adding markers...");
    var markerOptions = {
        position: loc,
        map: map
        // set icon
    };
    var marker = new google.maps.Marker(markerOptions);
}

// Determine appropriate bounds for view
function get_bounding_box_points() {
    var locLats = [];
    var locLongs = [];
    // loop through visible markers;
    for (i=0; i<places.length && i< maxPlaces; i++) {
        locLats.push(places[i].location.coordinate.latitude);
        locLongs.push(places[i].location.coordinate.longitude);
    }
    var points =  {
        'maxLat':Math.max.apply(null, locLats), 
        'minLat':Math.min.apply(null, locLats),
        'maxLong':Math.max.apply(null, locLongs), 
        'minLong':Math.min.apply(null, locLongs)
    };
    return points;
}

// Set the map bounds
function adjust_map_bounds() {
    if (places.length > 1) {
        var bounds = get_bounding_box_points();
        var SW = new google.maps.LatLng(bounds.minLat, bounds.minLong);
        var NE = new google.maps.LatLng(bounds.maxLat, bounds.maxLong);
        var mapBounds = new google.maps.LatLngBounds(SW, NE);
        map.fitBounds(mapBounds);
    }
}

// Search and map (driver function)
function get_and_map_places() {
    console.log("retrieving data...");
    var lat = "40.724925";
    var lon = "-73.9828847";
    initialize_current_location_on_map(lat, lon);
    var url = GET_search + "lat=" + lat + "&lon=" + lon + "&callback=handle_request";
    load_places_jspon_script(url);
}