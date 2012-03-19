import oauth2
import simplejson as json
import urllib
import urllib2
from datetime import date
import logging
logging.getLogger().setLevel(logging.INFO)
import pprint

import place
from utils import APIResponse
from utils import settings

REQUIRED_RESULTS = 5

YELP_WIFI_CAFE_SEARCH_TERM ='free+wifi+coffee'
YELP_ROOT_URL = 'http://api.yelp.com/v2/search?term='
YELP_BUSINESSES_TERM = "businesses"
YELP_RADIUS_METERS = 500
YELP_RADIUS_TERM = "&radius_filter=" + str(YELP_RADIUS_METERS)
YELP_LIMIT_NUM = 15
YELP_LIMIT_TERM = "&limit=" + str(YELP_LIMIT_NUM)
YELP_SORT_BY_BEST_MATCHED = 2
YELP_SORT_TERM = "&sort=" + str(YELP_SORT_BY_BEST_MATCHED)

FS_ROOT_URL = "https://api.foursquare.com/v2/venues/explore?"
FS_CAFE_SEARCH_TERM = "&section=coffee"

def do(term="", lat="", lon="", do_fs_search=False):
        
    check = checkparams(term, lat, lon)
    if check.has_key("error"):
        return check
        
    # yelp search
    yelp_results = get_yelp_results(term, lat, lon)
    # this is technically incorrect.
    # we should create a subclass of Exception called ApiMessage, and raise them
    if yelp_results.has_key("error"):
        return yelp_results
        
    if do_fs_search:
        fs_results = get_fs_results(lat, lon)
        results = merge_results(yelp_results, fs_results)
    else:
        results = yelp_results
        
    return results


def checkparams(term, lat, lon):
    if lat or lon:
        return APIResponse.API_SUFFICIENT_PARAMS
    else:
        return APIResponse.API_MISSING_PARAMS

def yelp_make_url(term, lat, lon):
    if not term:
        term = YELP_WIFI_CAFE_SEARCH_TERM
    url = (YELP_ROOT_URL +
        term + 
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

def get_response(url):
    try:
        conn = urllib2.urlopen(url, None)
        try:
            response = json.loads(conn.read())
        finally:
            conn.close()
    except urllib2.HTTPError, error:
        return APIResponse.YELP_API_NO_CONNECTION
    return response
        
def get_yelp_results(term, lat, lon):
    url = yelp_make_url(term, lat, lon)
    logging.info(url)
    signed_url = get_signed_url(url)
    logging.info(signed_url)
    response = get_response(signed_url)
    yelp_results = yelp_parse_response(response)
    logging.info(pprint.pformat(yelp_results))
    return yelp_results

def get_fs_results(lat, lon):
    url = fs_make_url(lat, lon)
    response = get_response(url)
    fs_results = fs_parse_response(response)
    return fs_results
    
def yelp_parse_response(response):
    results = {}
    places = response.get("businesses") or {}
    try:
        for p in places:
            if "phone" in p:
                phone = p.get('phone')
                results[phone] = p
    except Exception, e:
        logging.info("Error parsing yelp response: %s" % e)
        return APIResponse.YELP_API_INVALID_RESULTS
    return results

def fs_parse_response(fs_api_response):
    results = {}
    try:
        r = fs_api_response["response"]
        groups = r["groups"]
        groups = groups[0]
        items = groups["items"]
    except Exception, e:
        logging.info("Error parsing fs response: %s" % e)
        return APIResponse.FS_API_INVALID_RESULTS
        
    for item in items:
        venue = item.get("venue")
        if not (venue.get('contact') and venue['contact'].get('phone')):
            continue
        phone = venue["contact"]["phone"]
        results[phone] = venue
        results[phone]['tips'] = item.get('tips', {})
    
    return results

def merge_results(yelp_results, fs_results):
    merged_results = {}
        
    # both result sets have keys that are phone numbers
    yelp_phones = set(yelp_results.keys())
    fs_phones = set(fs_results.keys())
    # get the intersection of the two sets
    common_phones = yelp_phones & fs_phones
    # get the difference of the two sets
    uncommon_yelp_phones = yelp_phones - fs_phones
    uncommon_result_req = max(0, REQUIRED_RESULTS - len(common_phones))
    
    for cp in common_phones:
        if len(merged_results) < REQUIRED_RESULTS:
            merged_results[cp] = yelp_results.get(cp)
            fs_tips = fs_results.get(cp).get('tips')
            merged_results[cp]['tips'] = fs_tips
    
    if uncommon_result_req and uncommon_yelp_phones:
        for up in uncommon_yelp_phones:
            if len(merged_results) < REQUIRED_RESULTS:
                merged_results[up] = yelp_results.get(up)
                merged_results[up]['tips'] = {'text':'get on foursquare'}
    
    return merged_results
