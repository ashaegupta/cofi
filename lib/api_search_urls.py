import oauth2
import urllib
import urllib2
from datetime import date
import logging
logging.getLogger().setLevel(logging.INFO)
import pprint

from utils import APIResponse
from utils import settings

YELP_WIFI_CAFE_SEARCH_TERM ='free+wifi+coffee+shop'
YELP_ROOT_URL = 'http://api.yelp.com/v2/search?term='
YELP_BUSINESSES_TERM = "businesses"
YELP_RADIUS_METERS = 200
YELP_RADIUS_TERM = "&radius_filter=" + str(YELP_RADIUS_METERS)
YELP_LIMIT_NUM = 20
YELP_LIMIT_TERM = "&limit=" + str(YELP_LIMIT_NUM)
YELP_SORT_BY_BEST_MATCHED = 2
YELP_SORT_TERM = "&sort=" + str(YELP_SORT_BY_BEST_MATCHED)

FS_ROOT_URL = "https://api.foursquare.com/v2/venues/explore?"
FS_CAFE_SEARCH_TERM = "&section=coffee"

def check_params(lat, lon):
    if lat or lon:
        return APIResponse.API_SUFFICIENT_PARAMS
    else:
        return APIResponse.API_MISSING_PARAMS

def yelp_make_url(lat, lon):
    url = (YELP_ROOT_URL +
        YELP_WIFI_CAFE_SEARCH_TERM +
        "&ll=" + lat + "," + lon + 
        YELP_RADIUS_TERM + 
        YELP_LIMIT_TERM +
        YELP_SORT_TERM)
    return url
    
def fs_make_url(lat, lon):
    url = (FS_ROOT_URL + 
        "&ll=" + lat + "," + lon + 
        FS_CAFE_SEARCH_TERM + 
        "&client_id=" + settings.FS_CLIENT_ID + 
        "&client_secret=" + settings.FS_CLIENT_SECRET + 
        "&v=" + date.today().strftime("%Y%m%d"))
    return url
        
def get_signed_url(url):
    consumer = oauth2.Consumer(settings.YELP_CONSUMER_KEY, settings.YELP_CONSUMER_SECRET)
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                          'oauth_timestamp': oauth2.generate_timestamp(),
                          'oauth_token': settings.YELP_TOKEN,
                          'oauth_consumer_key': settings.YELP_CONSUMER_KEY})

    token = oauth2.Token(settings.YELP_TOKEN, settings.YELP_TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    return oauth_request.to_url()

def make(lat="", lon=""):
    check = check_params(lat, lon)
    if check.has_key("error"):
        return check
    urls = []
    yelp_url = yelp_make_url(lat=lat, lon=lon)
    urls.append(get_signed_url(yelp_url))
    urls.append(fs_make_url(lat, lon))
    return urls