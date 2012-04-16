var map;
var all_infowindows = [];

var GET_search = "/places?"
var places = [];
var maxPlaces = 20;

var current_lat;
var current_lon;
var chicago = new google.maps.LatLng(41.850033, -87.6500523);

/******************************** -- Map -- **************************************/

// Map current location
function initialize_current_location_on_map(lat, lon) {
    var options = {
      center: new google.maps.LatLng(lat, lon),
      zoom: 15,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      disableDefaultUI: true
    };
    map = new google.maps.Map(document.getElementById("map_canvas"),
        options);
    
    var refreshControlDiv = document.createElement('div');
    var refreshControl = new RefreshControl(refreshControlDiv, map);
    refreshControlDiv.index = 1;
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(refreshControlDiv);
    
    var addControlDiv = document.createElement('div');
    var addControl = new AddControl(addControlDiv, map);
    addControlDiv.index = 1;
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(addControlDiv);
    

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
    places = response.places;
    console.log("handling request...");
    map_places(places);
}

// Map places
function map_places(places){
    console.log(places);
    for (var p in places) {
        console.log("mapping places...");
        console.log(p);
        var lat = places[p].lat;
        var lon = places[p].lon;
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
    var phone = place.phone;
    display_phone = format_phone(phone);
    var position = [place.lat, place.lon];
    infoHTML = "<div style='font-family: \"Lucida Sans Typewriter\", Monaco, monospace; '>";
    infoHTML += "   <div style='font-weight:bold;'>";
    infoHTML +=     place.name;
    infoHTML += "   </div>";
    infoHTML += "   <div style='font-size:13px;margin-top:7px'>";
    infoHTML += "       <a href=callto:" + display_phone + ">";
    infoHTML +=         display_phone;
    infoHTML +=         "</a>";
    infoHTML += "   </div>";
    infoHTML += "   <div style='font-size:13px;margin-top:7px'>";
    infoHTML += "       <a href='";
    infoHTML += get_google_map_link(position);
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
        locLats.push(places[p].lat);
        locLongs.push(places[p].lon);
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
    alert('Almost ready to brew. Allow Cofi to access your location.');
}

// Search and map (driver function)
function get_and_map_places(position) {
    console.log("retrieving data...");
    var current_position = position.coords;
    current_lat = current_position.latitude;
    current_lon = current_position.longitude;
    initialize_current_location_on_map(current_lat, current_lon);
    var url = GET_search + "lat=" + current_lat + "&lon=" + current_lon + "&callback=handle_request";
    load_places_jspon_script(url);
}

function get_google_map_link(place_position) {
    var gurl = 'http://maps.google.com/maps?';
    var saddr = 'saddr=' + current_lat + "," + current_lon;
    var daddr = '&daddr=' + place_position[0] + "," + place_position[1];
    var mode = '&dirflg=w';
    return gurl + saddr + daddr + mode;
}

function format_phone(phone){
    return phone.substring(0,3) + "-" + phone.substring(3,6) + "-" + phone.substring(6);
}

function RefreshControl(controlDiv, map) {

    controlDiv.style.padding = '5px';
    
    // Set CSS for the control border
    var controlUI = document.createElement('div');
    controlUI.style.backgroundColor = 'pink';
    controlUI.style.borderStyle = 'solid';
    controlUI.style.padding = '5px';
    controlUI.style.borderWidth = '2px';
    controlUI.style.cursor = 'pointer';
    controlUI.style.textAlign = 'center';
    controlUI.title = 'Click to refresh the map';
    controlDiv.appendChild(controlUI);
    
    // Set CSS for the control interior
    var controlText = document.createElement('div');
    controlText.style.fontFamily = 'Arial,sans-serif';
    controlText.style.fontSize = '14px';
    controlText.style.paddingLeft = '4px';
    controlText.style.paddingRight = '4px';
    controlText.innerHTML = '<b>Refresh</b>';
    controlUI.appendChild(controlText);
    
    // Setup the click event listeners: simply set the map to
    // Chicago
    google.maps.event.addDomListener(controlUI, 'click', function() {
      current_lat = map.getCenter().lat();
      current_lon = map.getCenter().lng();
      var url = GET_search + "lat=" + current_lat + "&lon=" + current_lon + "&callback=handle_request";
      load_places_jspon_script(url);
    });
    
}

function AddControl(controlDiv, map) {

    controlDiv.style.padding = '5px';
    
    // Set CSS for the control border
    var controlUI = document.createElement('div');
    controlUI.style.backgroundColor = 'pink';
    controlUI.style.borderStyle = 'solid';
    controlUI.style.padding = '5px';
    controlUI.style.borderWidth = '2px';
    controlUI.style.cursor = 'pointer';
    controlUI.style.textAlign = 'center';
    controlUI.title = 'Click to refresh the map';
    controlDiv.appendChild(controlUI);
    
    // Set CSS for the control interior
    var controlText = document.createElement('div');
    controlText.style.fontFamily = 'Arial,sans-serif';
    controlText.style.fontSize = '14px';
    controlText.style.paddingLeft = '4px';
    controlText.style.paddingRight = '4px';
    controlText.innerHTML = '<b>+</b>';
    controlUI.appendChild(controlText);
    
    google.maps.event.addDomListener(controlUI, 'click', function() {
      map.setCenter(chicago)
    });
    
}



/******************************** -- Place Page -- **************************************/

// get the wifi, exp and plugs data if it exists
// set to this






