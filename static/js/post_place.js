// Steps

/** 
Server-side
1. Return success or error for GET and POST methods

Client-side
1. design interface, to receive an input

Review a place:
- Click Place
- 3 possible inputs:
    wifi
    cofi
    exp
- Submit
    Send: place_id, fs_id, or yelp_id
    Send: review

Add a place:
- Click plus sign
- Fs find a location.
- 3 possible inputs:
    wifi
    cofi
    exp
- Submit
    Send: fs_id
    Send: review

- Foursquare call

**/

var wifi;
var plugs;
var exp;

// Submit a place
$("save").click(function(){
  $.ajax({
      url:"/places?",
      data: ""{"fs_id":"19012",
             "wifi": '2'
            }"",
      success:function(result){
          // Got it! fade
          $("fade").html(result);
      },
      error:function(result){
          $("div").html(result)
      }
  });

// Review a place
$("review").click(function(){
$.ajax({
    url:"/places?",
    data: ""{"yelp_id":"19012",
           "wifi": '2'
          }"",
    success:function(result){
        // Got it! fade
        // Update visual
        $("fade").html("Got it!");
    },
    error:function(result){
        $("div").html(result)
    }
});

// Refresh place for a bounding box or for current location
$("refresh").click(function(){
$.ajax({
    url:"/places?",
    data: ""{"yelp_id":"19012",
           "wifi": '2'
          }"",
    success:function(result){
        // show the places
        $("fade").html("Got it!");
    },
    error:function(result){
        $("div").html(result)
    }
});