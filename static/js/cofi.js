var map;
var all_infowindows = [];

var GET_cofi_places = "/places?"
var GET_fs_search = "/fs?"
var POST_cofi_places = "/places"
var places = [];
var maxPlaces = 20;

var current_lat;
var current_lon;
var adjust_map_bounds_control = true;

/******************************** Global Configurations for Jquery Mobile ************************/

$(document).bind("mobileinit", function(){
  $.mobile.orientationChangeEnabled = false;
  $.mobile.loadingMessage = "brewing";
  $.mobile.pageLoadErrorMessage = "Whoopsies. There's been an error.";
});




/******************************** Create Map **************************************/

// Map current location
function initialize_current_location_on_map(lat, lon) {
    var options = {
      center: new google.maps.LatLng(lat, lon),
      zoom: 15,
      disableDefaultUI: true,
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
    if (adjust_map_bounds_control){
        adjust_map_bounds();
    }
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
    var url = GET_cofi_places + "lat=" + current_lat + "&lon=" + current_lon + "&callback=handle_request";
    load_places_jspon_script(url);
}

// Refresh the map once the user has moved it
function refresh() {
    current_lat = map.getCenter().lat();
    current_lon = map.getCenter().lng();
    var url = GET_cofi_places + "lat=" + current_lat + "&lon=" + current_lon + "&callback=handle_request";
    adjust_map_bounds_control = false;
    load_places_jspon_script(url);
}

// Make google map link for a given position
function get_google_map_link(place_position) {
    var gurl = 'http://maps.google.com/maps?';
    var saddr = 'saddr=' + current_lat + "," + current_lon;
    var daddr = '&daddr=' + place_position[0] + "," + place_position[1];
    var mode = '&dirflg=w';
    return gurl + saddr + daddr + mode;
}

// Format the phone to xxx-xxx-xxxx
function format_phone(phone){
    return phone.substring(0,3) + "-" + phone.substring(3,6) + "-" + phone.substring(6);
}


/******************************** Add Place **************************************/

// Find nearby places
function fs_search() {
    var query = $("#fs_list").prev('form[role="search"]').find('input[data-type="search"]').val();
    var data = {
        "lat":current_lat,
        "lon":current_lon
    };
    if (query) {
        data["query"]=encodeURIComponent(query);
    }
    $.get(GET_fs_search, data, function(resp) {
        var json = jQuery.parseJSON(resp);
        console.log("Response JSON: ", json);
        var venues = json.response.venues;
        document.getElementById("fs_list").innerHTML = create_fs_list_html(venues);
    });
}

// Makes the data_object and returns the HTML for a fs_list
function create_fs_list_html(venues) {
    var fs_list_html = "";
    for (i=0; i<venues.length; i++) {
        var venue = venues[i];
        parse_and_add_fs_venue_to_local_storage(venue);
        fs_list_html += create_fs_list_element(id=venue.id, name=venue.name);
    }
    
    return fs_list_html;
}

// Parse and add fs object to local storage
function parse_and_add_fs_venue_to_local_storage(venue){
    var data_object = {};
    data_object.id = venue.id;
    data_object.name = venue.name;
    data_object.address = venue.location.address;
    data_object.lat = venue.location.lat;
    data_object.lon = venue.location.lng;
    
    if ("phone" in venue.contact) {
        data_object.phone = venue.contact.phone;
    }
    
    var data_object_str = JSON.stringify(data_object);
    localStorage.setItem(data_object.id, data_object_str);
}


// Write html for an element in the fs list
function create_fs_list_element(id, name) {
    var id_type = 'fs_id';
    var element_html =  "<li data-corners=\"false\" data-shadow=\"false\" data-iconshadow=\"true\" data-wrapperels=\"div\"";
    element_html += "data-icon=\"arrow-r\" data-iconpos=\"right\" data-theme=\"c\"";
    element_html += "class=\"ui-btn ui-btn-icon-right ui-li-has-arrow ui-li ui-corner-bottom ui-btn-up-c\">";
    element_html += "<div class=\"ui-btn-inner ui-li\"><div class=\"ui-btn-text\">";
    
    element_html += "<a href=\"#review\"";
    element_html += " data-transition=\"slide\""; 
    element_html += " onclick=\"make_review_form("; 
    element_html += "id='" + id + "', id_type='" + id_type + "'); return false\" class=\"ui-link-inherit\">";
    element_html += name + "</a></div></div></li>";
    
    return element_html;
}

// Prepares the form
function make_review_form(id, id_type){
    var place_data_object_str = localStorage.getItem(id);
    var place_data_object = JSON.parse(place_data_object_str);
    document.getElementById("review_header").innerHTML = "Review " + place_data_object.name;
    document.getElementById("review_place_id").value = id;
    document.getElementById("review_place_id").name = id_type;
    $("input[type='radio']").prop("checked",false).checkboxradio("refresh");
}

function post_review(){
    // Get review form elements
    var review_data_dict = {};
    var review_data_str = $('#review_form').serializeArray();
    $.each(review_data_str, function(i, field){
       review_data_dict[field.name] = field.value;
     });
     
    // Get place data from localstorage elements
    var id = document.getElementById('review_place_id').value;
    var place_data_object_str = localStorage.getItem(id);
    var place_data_object = JSON.parse(place_data_object_str);
    review_data_dict.name = place_data_object.name;
    review_data_dict.lat = place_data_object.lat;
    review_data_dict.lon = place_data_object.lon;
    review_data_dict.address = place_data_object.address;
    
    if ("phone" in place_data_object){
        review_data_dict.phone = place_data_object.phone;
    }
    
    console.log("review_data_dict", review_data_dict);
    $.ajax({
        type: 'POST',
        url: POST_cofi_places,
        data: review_data_dict,
        success: function(data) {
             console.log(data);
             alert("success" ); 
        }
    });
}
