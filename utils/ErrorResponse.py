API_MISSING_PARAMS = {
    'error':1,
    'message':'Insufficient search terms'
}

API_SUFFICIENT_PARAMS = {
    'success':1,
    'message':'Sufficient search terms'
}

YELP_API_INVALID_RESULTS = {
    'error':1,
    'message':'Invalid results from Yelp'
}

YELP_API_NO_CONNECTION = {
    'error':1,
    'message':'Unable to connect to Yelp API'
}


FS_API_INVALID_RESULTS = {
    'error':1,
    'message':'Invalid results from foursquare API'
}


POST_INVALID_ARGS_FS_ID_YELP_ID = {
    'error':1,
    'message':'Does not have fs_id or yelp_id',
}

POST_INVALID_ARGS_LOC_DATA = {
    'error':1,
    'message':'Does not have sufficient place data',
}