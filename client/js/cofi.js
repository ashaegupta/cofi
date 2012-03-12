var map;
var GET_search_url_root="http://splitmyri.de/cofi?"

// Map current location
function initialize(lat, lon) {
    var options = {
      center: new google.maps.LatLng(lat, lon),
      zoom: 12,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("map_canvas"),
        options);
}

// Get & map places
function find_and_map_places(lat, lon) {
    url = GET_search_url_root + "lat=" + lat + "&lon=" + lon + "&callback=load_places"
    load_places_script(url)
}

// A jsonp request script
function load_places_script(url) {
    /* makes a jsonp request for _src */
    var e = document.createElement('script');
    e.setAttribute('language','javascript'); 
    e.setAttribute('type', 'text/javascript');
    e.setAttribute('src', url); 
    var parent = document.head;
    parent.appendChild(e);
}

// Callback function for load_places_script. Also parses json response to return list of places
function load_places(response) {
    places = response.data();
    return places;
}

// Map places
function map_places(places){
    for (i=0; i<places.length, i++){
        var lat = places[i].coordinate.latitude;
        var lat = places[i].coordinate.longitude;
        var loc = new google.maps.LatLng(lat,lon);
        new add_marker(loc)
    }
}

// Set marker characteristics
function add_marker(loc){
    var markerOptions = {
        position: loc;
        map: map;
        // set icon
    }
    var marker = new google.maps.Marker(markerOptions);
}
    