from model.Place import Place
import requests
import simplejson as json
from lib import place_handler

def test_post():
    if not Place.mdbc().count() == 0:
        Place.mdbc().remove()

    # Add new place
    url = "http://localhost/places"
    payload = {
            "fs_id" : 'aslfkj13409182491k1we1-12e801',
            "name" :  'Ninth Street Espresso',
            "phone" : '2129201880',
            "lat" : '42.881111',
            "lon" : '78.191111',
            "address" : '180 Crosby Street',
            "wifi" : '2',
            "plugs" : '1'
    }
    r = requests.post(url=url, data=payload)
    spec = r.content
    spec_js = json.loads(spec)
    place_id = spec_js.get('place_id')
    
    # Add another review to previous place
    payload = {
                "place_id" : place_id,
                "wifi" : '0',
                "plugs" : '0'
                
    }
    r = requests.post(url=url, data=payload)

    # Add another review to previous place
    payload = {
                "place_id" : place_id,
                "wifi" : '0',
                "plugs" : '0'
                
    }
    r = requests.post(url=url, data=payload)
    
    # Add new place
    payload = {
            "fs_id" : '12e801',
            "name" :  'The Bean',
            "phone" : '2129201881',
            "lat" : '42.881111',
            "lon" : '78.191111',
            "address" : '180 Crosby Street',
            "wifi" : '2',
            "plugs" : '1'
    }
    r = requests.post(url=url, data=payload)
    r.content
    
    # Add new place
    payload = {
            "fs_id" : '12801',
            "name" :  'The Native Bean',
            "phone" : '2129202880',
            "lat" : '42.881111',
            "lon" : '78.191111',
            "address" : '180 Crosby Street',
            "wifi" : '1',
            "plugs" : '1'
    }
    r = requests.post(url=url, data=payload)
    r.content
    
    # Add new place
    payload = {
            "fs_id" : '12801',
            "name" :  'Gimme Coffee',
            "phone" : '2129201980',
            "lat" : '42.881111',
            "lon" : '78.191111',
            "address" : '180 Crosby Street',
            "wifi" : '0',
            "plugs" : '1'
    }
    r = requests.post(url=url, data=payload)
    r.content
    
    # Add new place
    payload = {
            "fs_id" : '12801',
            "name" :  'Gimme Coffee Now',
            "phone" : '3129201980',
            "lat" : '43.881111',
            "lon" : '79.191111',
            "address" : '180 Crosby Street',
            "wifi" : '0',
            "plugs" : '1'
    }
    r = requests.post(url=url, data=payload)
    r.content
    print 'Database_count = ' + str(Place.mdbc().count())

def test_get():
    lat = '42.881111'
    lon = '78.191111'
    places = place_handler.get_places(lat=lat, lon=lon)
    return places