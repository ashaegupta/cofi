import simplejson as json
from model.Place import Place

def yelp(resp):
    output = {}
    
    # Grab the necessary top level keys from the yelp resp and add to output
    yelp_keys_and_db_keys = {
                            'phone':Place.A_PHONE,
                            'id': Place.A_YELP_ID,
                            'name': Place.A_NAME,
                            'review_count': Place.A_YELP_REVIEW_COUNT,
                            'rating_img_url_small': Place.A_YELP_RATING
    }
    for yelp_key, db_key in yelp_keys_and_db_keys.iteritems():
        value = resp.get(yelp_key)
        if value:
            output[db_key] = value
    
    # Go through the location dict and add necessary data to output
    location = resp.get('location')
    if location:
        coordinate = location.get('coordinate')
        if coordinate:
            output[Place.A_LAT] = coordinate.get('latitude')
            output[Place.A_LON] = coordinate.get('longitude')
        address = location.get('address')
        if address:
            output[Place.A_ADDRESS] = address[0]    
    
    # Set the default to unlimited wifi
    output[Place.A_RECOS] = {}
    output[Place.A_RECOS][Place.A_WIFI] = Place.A_HIGH
    
    print output
    return output
    