from lib import place_handler
from model.Place import Place

fs_id = 'aslfkj13409182491k1we1-12e801'
name =  'Ninth Street Espresso'
phone = '2129201880'
lat = 42.88
lon = 78.19
address = '180 Crosby Street'
wifi = '0'
plugs = '1'

place_id = place_handler.add_place(fs_id=fs_id, name=name, phone=phone, lat=lat, lon=lon, address=address, wifi=wifi, plugs=plugs)

Place.mdbc().count()
Place.mdbc().find_one({'place_id': place_id})

wifi = '1'
exp = '1'
plugs = '0'

place_handler.review_place(place_id=place_id, wifi=wifi, plugs=plugs, exp=exp)
Place.mdbc().count()
Place.mdbc().find_one({'place_id': place_id})


wifi = None
exp = None
plugs = None

place_handler.review_place(place_id=place_id, wifi=wifi, plugs=plugs, exp=exp)
Place.mdbc().count()
Place.mdbc().find_one({'place_id': place_id})

fs_id = None
name =  'Ninth Street Espresso'
phone = '2139201880'
lat = 42.88
lon = 78.19
address = '180 Crosby Street'
wifi = '0'
plugs = '1'

place_id = place_handler.add_place(fs_id=fs_id, name=name, phone=phone, lat=lat, lon=lon, address=address, wifi=wifi, plugs=plugs)

Place.mdbc().count()
Place.mdbc().find_one({'place_id': place_id})
