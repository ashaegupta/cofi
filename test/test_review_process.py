from model.Place import Place
import requests
import simplejson as json

url = "http://localhost/places"
payload = {
        "fs_id" : 'aslfkj13409182491k1we1-12e801',
        "name" :  'Ninth Street Espresso',
        "phone" : '2129201880',
        "lat" : '42.88',
        "lon" : '78.19',
        "address" : '180 Crosby Street',
        "wifi" : '0',
        "plugs" : '1'
}

r = requests.post(url=url, data=payload)
r.content
place_dict = json.loads(r.content)
place_id = place_dict.get('place_id')
Place.mdbc().count()
Place.mdbc().find_one({'place_id': place_id})

payload = {
        'place_id': place_id, 
        "wifi" : '1',
        "exp" :'1',
        "plugs" : '0'
}

r = requests.post(url=url, data=payload)
r.content
place_dict = json.loads(r.content)
place_id = place_dict.get('place_id')
Place.mdbc().count()
Place.mdbc().find_one({'place_id': place_id})
