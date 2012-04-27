import sys
sys.path.append("../")
import logging
import uuid
import datetime
import time
import MongoMixIn
from utils import settings

# Can I remove this class wrapper?
class Place(MongoMixIn.MongoMixIn):    
    MONGO_DB_NAME           = 'place'
    
    if settings.ON_TEST:
        MONGO_COLLECTION_NAME = 'place_c_test'
    else:
        MONGO_COLLECTION_NAME = 'place_c'
    
    # Top level attributes
    A_PLACE_ID                      = 'place_id'
    A_FS_ID                         = 'fs_id'
    A_YELP_ID                       = 'yelp_id'
    A_PHONE                         = 'phone'
    A_NAME                          = 'name'
    A_ADDRESS                       = 'address'
    A_LAT                           = 'lat'
    A_LON                           = 'lon'
    A_LOCATION                      = 'loc'                       # [lat, lon] 
    A_REVIEW                        = 'review'                    # single incoming review; a dict, see sub attributes below
    A_ALL_REVIEWS_RAW               = 'all_reviews_raw'           # list of raw reviews
    A_ALL_REVIEWS_SUM               = 'all_reviews_sum'           # summary count of each review
    A_RECOS                         = 'recos'                     # recommendations based on reviews
    A_YELP_RATING                   = 'yp_rating'
    A_YELP_REVIEW_COUNT             = 'yp_review_count'
    A_CREATED_TS                    = 'created_ts'
    A_UPDATED_TS                    = 'updated_ts'
    
    
    # Sub attributes under review dictionary and wifi, exp, plugs are first level under recommendation data
    A_WIFI                       = 'wifi'
    A_EXP                        = 'exp'
    A_PLUGS                      = 'plugs'
    A_REVIEWER                   = 'reviewer'
    A_CREATED_REVIEW_TS          = 'created_review_ts'
    
    # Second level under recommendation data for wifi, exp, plugs keys
    A_LOW                        = '0'                      # wifi = None, experience = Poor, plugs = None
    A_MED                        = '1'                      # wifi = Limited, experience = Okay
    A_HIGH                       = '2'                      # wifi = Unlimited, experience = Great
    A_COUNT                      = 'count'                  # total reviews
    
    MILES_PER_DEGREE                = 69                    # miles
    MAX_SEARCH_DISTANCE_IN_MILES    = 0.5                   # miles
    MAX_SEARCH_DISTANCE_IN_DEGREES  = float(MAX_SEARCH_DISTANCE_IN_MILES/MILES_PER_DEGREE)
    RESULTS_LIMIT                   = 20
    
    @classmethod
    def setup_mongo_indexes(klass):
        from pymongo import ASCENDING
        from pymongo import GEO2D
        coll = klass.mdbc()
        coll.ensure_index([(klass.A_PHONE, ASCENDING)], unique=True)
        coll.ensure_index([(klass.A_PLACE_ID, ASCENDING)], unique=True)
        coll.ensure_index([(klass.A_FS_ID, ASCENDING)], unique=True)
        coll.ensure_index([(klass.A_YELP_ID, ASCENDING)], unique=False)
        coll.ensure_index([(klass.A_LOCATION, GEO2D)], unique=False)
    
    @classmethod
    def get_places(klass, lat=None, lon=None, box=None):
        if not ((lat and lon) or box):
            return None
        
        if lat and lon:
            loc = [float(lat), float(lon)]
            spec = {klass.A_LOCATION:{"$within":{"$center":[loc, klass.MAX_SEARCH_DISTANCE_IN_DEGREES]}}}
        if box:
            spec = {klass.A_LOCATION:{"$within":{"$box":box}}}
        
        cursor = klass.mdbc().find(spec).limit(klass.RESULTS_LIMIT)
        return klass.list_from_cursor(cursor, remove_object_id=True)
    
    @classmethod
    def review_place(klass, place_id, review=None):
        """review a place that exists in the database.
        place_id is the cofi id, different from fs or yelp.
        """
        if not review:
            return None
        
        # process the review  
        doc = klass.process_review(review)
        
        # update timestamp
        if '$set' not in doc:
            doc['$set'] = {}
        
        doc["$set"][klass.A_UPDATED_TS] = int(time.time())
        
        # update the database
        return klass.update(place_id=place_id, doc=doc)
    
    @classmethod
    def add_place(klass, place_data, review):
        """add a new place and one review to the database
        """
        doc = {}
        
        place_id = uuid.uuid4().hex
        set_doc = {
            klass.A_PLACE_ID: place_id,
            klass.A_CREATED_TS: int(time.time()),
            klass.A_UPDATED_TS: int(time.time())
        }
        set_doc.update(place_data)
        doc["$set"] = set_doc
        
        # process the review if it exists
        if review:
            review_doc = klass.process_review(review)
            doc.update(review_doc)
        
        # update the database
        return klass.update(place_id=place_id, doc=doc)
    
    
    # Helper method to process incoming review and update recommendation data
    @classmethod
    def process_review(klass, review):
        review_doc = {}
        
        # add timestamp for review
        review[klass.A_CREATED_REVIEW_TS] = int(time.time())
        
        # add review to list
        review_doc["$push"] = {klass.A_ALL_REVIEWS_RAW:review}
        
        # for each attribute, value in the review, increment value count in reco data
        inc_doc = {}
        
        for attribute, value in review.iteritems():
            if klass.value_is_valid_reco_dict_key(value):
                value_path = klass.A_ALL_REVIEWS_SUM + "." + attribute + "." + value 
                count_path = klass.A_ALL_REVIEWS_SUM + "." + attribute + "." + klass.A_COUNT
                inc_doc[value_path] = 1
                inc_doc[count_path] = 1
              
        if inc_doc:
            review_doc["$inc"] = inc_doc
          
        return review_doc
    
    
    # Ensure value is a valid key in the recommendation dictionary
    @classmethod  
    def value_is_valid_reco_dict_key(klass, value=None):
        if value in [klass.A_HIGH, klass.A_MED, klass.A_LOW]:
            return True
        else:
            return False
    
    # Update the database for a given place_id
    @classmethod
    def update(klass, place_id, doc):
        spec = {klass.A_PLACE_ID:place_id}
        try:
            klass.mdbc().update(spec=spec, document=doc, upsert=True, safe=True)
        except Exception, e:
            logging.error("COULD NOT UPSERT document in model.Place Exception: %s" % e.message)
            return False
        return spec
