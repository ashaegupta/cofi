import simplejson as json

from utils import ErrorResponse
from model.Place import Place

MUST_HAVE_WIFI = True
MUST_HAVE_PLUGS = True

############# POST HELPER METHODS ################
def add_place(name, phone, lat, lon, address, fs_id=None, yelp_id=None, wifi=None, plugs=None, exp=None):
    # ensure it has a fs_id or a yelp_id
    if not (fs_id or yelp_id):
        return ErrorResponse.POST_INVALID_ARGS_FS_ID_YELP_ID
    
    # Create a review dict
    review = make_review_dict(wifi, plugs, exp)  
    
    # Check if place already exists in the database
    if fs_id:
        spec = {Place.A_FS_ID: fs_id}
        place_dict = Place.mdbc().find_one(spec)
        
        # If place exists add a review to it
        if place_dict:
            place_id = place_dict.get(Place.A_FS_ID)
            return Place.review_place(place_id=place_id, review=review)
        
    # If place doesn't already exist in the database add it
    place_data = {
          Place.A_NAME: name,
          Place.A_FS_ID: fs_id,
          Place.A_YELP_ID: yelp_id,
          Place.A_ADDRESS: address,
          Place.A_LOCATION: [float(lat), float(lon)]
    }
    
    # Only add phone if it's not null
    if phone:
        place_data[Place.A_PHONE] = phone
    
    return Place.add_place(place_data=place_data, review=review)
    
def review_place(place_id, wifi=None, plugs=None, exp=None):
    review = make_review_dict(wifi, plugs, exp)
    return Place.review_place(place_id=place_id, review=review)

def make_review_dict(wifi, plugs, exp):
    review = {}
    if wifi:
        review[Place.A_WIFI] = wifi
    if plugs and not plugs == "-1":
        review[Place.A_PLUGS] = plugs
    if exp:
        review[Place.A_EXP] = exp
    return review


############# GET HELPER METHODS ################
def get_places_from_db(lat=None, lon=None, x_1=None, x_2=None, y_1=None, y_2=None,
                filter_by_wifi=MUST_HAVE_WIFI, filter_by_plugs=MUST_HAVE_PLUGS):
    if not (lat and lon) and not (x_1 and x_2 and y_1 and y_2):
        return ErrorResponse.GET_INVALID_ARGS
    
    if (lat and lon):
        places = Place.get_places(lat=lat, lon=lon)
    if (x_1 and x_2 and y_1 and y_2):
        box = [[x_1, y_1], [x_2, y_2]]
        places = Place.get_places(box=box)
    
    places_output = process_places_from_db(places, filter_by_wifi=filter_by_wifi, filter_by_plugs=filter_by_plugs)
    return places_output
    
def process_places_from_db(places, filter_by_wifi, filter_by_plugs):
    if not places:
        return None
        
    places_output = []
    for place_input in places:
        reviews = place_input.get(Place.A_ALL_REVIEWS_SUM)
        recos = make_recos_from_reviews(reviews)
        
        if filter_by_wifi:
            wifi_score = recos[Place.A_WIFI]
            if wifi_score == Place.A_LOW or wifi_score == Place.A_MED:
                continue
        if filter_by_plugs:
            plugs_score = recos[Place.A_PLUGS]
            if plugs_score == Place.A_LOW:
                continue

        place_output = make_place_output(place_input, recos)
        places_output.append(place_output)

    return places_output

def make_recos_from_reviews(place_reviews=None):
    if not place_reviews:
        place_reviews={}
    recos={}
    for attribute, reviews in place_reviews.iteritems():
        if attribute in [Place.A_WIFI, Place.A_PLUGS, Place.A_EXP]:
            most_freq_score = None
            for score, count in reviews.iteritems():
                if score in [Place.A_LOW, Place.A_MED, Place.A_HIGH]:
                    if not most_freq_score:
                        most_freq_score = score
                    elif count > reviews.get(most_freq_score):
                        most_freq_score = score
            if most_freq_score:
                recos[attribute] = most_freq_score
    return recos

def make_place_output(place_input, recos=None):
    place_output={}
    output_keys = [Place.A_PLACE_ID,Place.A_NAME, Place.A_PHONE, Place.A_ADDRESS]
    for k in output_keys:
        place_output[k] = place_input[k]
    loc = place_input[Place.A_LOCATION]
    place_output[Place.A_LAT] = loc[0]
    place_output[Place.A_LON] = loc[1]
    
    if recos:
        place_output[Place.A_RECOS] = recos
    return place_output
