import oauth2
import simplejson as json
import urllib
import urllib2
from datetime import date

import place
from utils import APIResponse
from utils import settings

YELP_WIFI_CAFE_SEARCH_TERM ='wifi+cafe'
YELP_ROOT_URL = 'http://api.yelp.com/v2/search?term='
YELP_BUSINESSES_TERM = "businesses"

FS_ROOT_URL = "https://api.foursquare.com/v2/venues/explore?"
FS_CAFE_SEARCH_TERM = "&section=coffee"
FS_SEARCH_RADIUS = "&radius=2000"
DO_FS_SEARCH = False

def do(term="", lat="", lon=""):
    
    if term:
        do_fs_search = False
    else:
        do_fs_search = DO_FS_SEARCH
        
    check = checkparams(term, lat, lon)
    if check.has_key("error"):
        return check
        
    # yelp search
    url = yelp_make_url(term, lat, lon)
    signed_url = get_signed_url(url)
    response = get_response(signed_url)
    yelp_results = yelp_parse_response(response)
    if yelp_results.has_key("error") or not do_fs_search:
        return yelp_results
        
    if do_fs_search:
        url = fs_make_url(lat, lon)
        response = get_response(url)
        merged_results = fs_parse_response(response, yelp_results)
        return merged_results

def checkparams(term, lat, lon):
    if lat or lon:
        return APIResponse.API_SUFFICIENT_PARAMS
    else:
        return APIResponse.API_MISSING_PARAMS

def yelp_make_url(term, lat, lon):
    if not term:
        term = YELP_WIFI_CAFE_SEARCH_TERM
    url = YELP_ROOT_URL + term + "&ll=" + lat + "," + lon
    return url
    
def fs_make_url(lat, lon):
    return FS_ROOT_URL + "&ll=" + lat + "," + lon + FS_CAFE_SEARCH_TERM + FS_SEARCH_RADIUS + "&client_id=" + settings.FS_CLIENT_ID + "&client_secret=" + settings.FS_CLIENT_SECRET + "&v=" + date.today().strftime("%Y%m%d")

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

def get_response(signed_url):
    # Connect
      try:
        conn = urllib2.urlopen(signed_url, None)
        try:
          response = json.loads(conn.read())
        finally:
          conn.close()
      except urllib2.HTTPError, error:
        return APIResponse.YELP_API_NO_CONNECTION
      return response
    
def yelp_parse_response(response):
    results = {}
    results["data"] = []
    results["has_fs_results"] = False
    no_phone_count = 0
    places = response.get("businesses")
    print len(places)
    try:
        for p in places:
            results["data"].append(p)
    except:
        return APIResponse.YELP_API_INVALID_RESULTS
    return results

def fs_parse_response(response, yelp_results):
    results = {}
    results["body"] = []
    results["has_ordered_results"] = True
    try:
        r = response["response"]
        groups = r["groups"]
        groups = groups[0]
        items = groups["items"]
        for item in items:
            venue = item["venue"]
            try: 
                phone = venue["contact"]["phone"]
                if yelp_results["body"].has_key(phone):
                    place = {}
                    place[phone] = json.loads(yelp_results["body"][phone])
                    tips = item["tips"]
                    tips = tips[0]
                    tip = tips["text"]
                    place[phone]["tips"] = tip
                    results["body"].append(place)
            except:
                pass
    except:
        return APIResponse.FS_API_INVALID_RESULTS
    return results

