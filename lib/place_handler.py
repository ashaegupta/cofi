from model.Place import Place
from utils import ErrorResponse

def add_place(name, phone, lat, lon, address, fs_id=None, yelp_id=None, wifi=None, plugs=None, exp=None):
    # ensure it has a fs_id or a yelp_id
    if not (fs_id or yelp_id):
        return ErrorResponse.POST_INVALID_ARGS_FS_ID_YELP_ID
      
    location = {
        Place.A_LAT:float(lat), 
        Place.A_LON:float(lon),
        Place.A_ADDRESS: address
    }
    
    review = make_review_dict(wifi, plugs, exp)  
    
    place_data = {
          Place.A_NAME: name,
          Place.A_PHONE: phone,
          Place.A_FS_ID: fs_id,
          Place.A_YELP_ID: yelp_id,
          Place.A_LOCATION: location
    }
    
    return Place.add_place(place_data=place_data, review=review)
    
def review_place(place_id, wifi=None, plugs=None, exp=None):
    review = make_review_dict(wifi, plugs, exp)
    return Place.review_place(place_id=place_id, review=review)

def make_review_dict(wifi, plugs, exp):
    review = {}
    if wifi:
        review[Place.A_WIFI] = wifi
    if plugs:
        review[Place.A_PLUGS] = plugs
    if exp:
        review[Place.A_EXP] = exp
    return review