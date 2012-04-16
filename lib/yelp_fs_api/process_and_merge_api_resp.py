import simplejson as json
import logging
logging.getLogger().setLevel(logging.INFO)
import pprint

import format_api_resp
from utils import ErrorResponse
from utils import settings

REQUIRED_RESULTS = 5

def yelp_parse_response(response):
    results = {}
    places = response.get("businesses") or {}
    try:
        for p in places:
            if "phone" in p:
                phone = p.get('phone')
                results[phone] = format_api_resp.yelp(p)
    except Exception, e:
        logging.info("Error parsing yelp response: %s" % e)
        return ErrorResponse.YELP_API_INVALID_RESULTS
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
        return ErrorResponse.FS_API_INVALID_RESULTS
        
    for item in items:
        venue = item.get("venue")
        if not (venue.get('contact') and venue['contact'].get('phone')):
            continue
        phone = venue["contact"]["phone"]
        results[phone] = venue
        #results[phone]['tips'] = item.get('tips', {})
    
    return results

def merge(yelp_results, fs_results):
    merged_results = []
        
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
            cp_place_data = yelp_results.get(cp)
            merged_results.append(cp_place_data)
            # fs_tips = fs_results.get(cp).get('tips')
            # merged_results[cp]['tips'] = fs_tips
    
    if uncommon_result_req and uncommon_yelp_phones:
        for up in uncommon_yelp_phones:
            if len(merged_results) < REQUIRED_RESULTS:
                up_place_data = yelp_results.get(up)
                merged_results.append(up_place_data)
                # merged_results[up]['tips'] = {'text':'No tips. This place needs to get on foursquare'}
    
    return merged_results

def process(responses):
    for r in responses:
        if r.has_key("error"):
            return r
        else:
            
            # Set the responses appropriately
            if responses[0].has_key("businesses"):
                yelp_response = responses[0]
                fs_response = responses[1]
            elif responses[1].has_key("businesses"):
                yelp_response = responses[1]
                fs_response = responses[0]
            else:
                return ErrorResponse.YELP_API_INVALID_RESULTS
            
            # Parse the responses    
            yelp_results = yelp_parse_response(yelp_response)
            fs_results = fs_parse_response(fs_response)
            
            # Merge the responses
            return merge(yelp_results, fs_results)