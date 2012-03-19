var map;
var all_infowindows = [];

var GET_search = "/cofi/places?"
var places = [];
var maxPlaces = 20;

var current_position;

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
    console.log(places);
    for (var p in places) {
        console.log("mapping places...");
        console.log(p);
        var lat = places[p].location.coordinate.latitude;
        var lon = places[p].location.coordinate.longitude;
        console.log(places[p].name);
        var loc = new google.maps.LatLng(lat,lon);
        var marker = add_marker(loc);
        infowindow = create_infowindow(marker, places[p]);
        all_infowindows.push(infowindow);
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
    return marker;
}

// Returns the HTML for an infowindow
function create_infowindow(marker, place) {
    console.log(place);
    var phone = place.display_phone.replace("+1-","");
    infoHTML = "<div style='font-family: \"Lucida Sans Typewriter\", \"Lucida Console\", Monaco, \"Bitstream Vera Sans Mono\", monospace;'>";
    infoHTML += "   <div>";
    infoHTML +=     place.name;
    infoHTML += "   </div>";
    infoHTML += "   <div style='font-size:13px;margin-top:10px'>";
    infoHTML += "       <a href=callto:" + phone + ">";
    infoHTML +=         phone;
    infoHTML +=         "</a>";
    infoHTML += "   </div>";
    infoHTML += "   <div style='font-size:13px;margin-top:10px'>";
    infoHTML += "       <a href='";
    infoHTML += get_google_map_link(place.location.coordinate);
    infoHTML += "       '>Show directions</a>";
    infoHTML += "   </div>";
    infoHTML += "</div>";
    var infowindow = new google.maps.InfoWindow({content: infoHTML, maxWidth: 120});
    // add click listener on the marker, to show the infowindow
    google.maps.event.addListener(marker, 'click', function() {
        close_all_info_windows();
        infowindow.open(map, marker);
    });
    return infowindow;
}

function close_all_info_windows() {
    // goes through a global list of all infowindows and closes them
    for (i=0; i<all_infowindows.length; i++) {
        all_infowindows[i].close();
    }
}

// Determine appropriate bounds for view
function get_bounding_box_points() {
    var locLats = [];
    var locLongs = [];
    // loop through visible markers;
    for (var p in places) {
    //for (i=0; i<places.length && i< maxPlaces; i++) {
        locLats.push(places[p].location.coordinate.latitude);
        locLongs.push(places[p].location.coordinate.longitude);
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


// Driver methods. Start_cofi is the first method that runs to find location
// If success, continue to get_and_map_places, else return an error.
function start_cofi(){
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(get_and_map_places, no_position);
    } else {
        no_position('not supported');
    }
}

function no_position(msg) {
    alert(msg);
}

// Search and map (driver function)
function get_and_map_places(position) {
    console.log("retrieving data...");
    current_position = position.coords;
    var lat = current_position.latitude;
    var lon = current_position.longitude;
    initialize_current_location_on_map(lat, lon);
    var url = GET_search + "lat=" + lat + "&lon=" + lon + "&callback=handle_request";
    load_places_jspon_script(url);
}

function get_google_map_link(place_position) {
    var gurl = 'http://maps.google.com/maps?';
    var saddr = 'saddr=' + current_position.latitude + "," + current_position.longitude;
    var daddr = '&daddr=' + place_position.latitude + "," + place_position.longitude;
    var mode = '&dirflg=w';
    return gurl + saddr + daddr + mode;
}
