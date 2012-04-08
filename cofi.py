import os
import re
import tornado
import tornado.httpserver
import tornado.autoreload
import tornado.escape
import tornado.httpclient
import tornado.ioloop
import tornado.web
import simplejson as json
import logging

from lib.yelp_fs_api import api_search_urls, api_responses
from lib import place_handler
from model.Place import Place

class PlacesHandler(tornado.web.RequestHandler):
    
    @tornado.web.asynchronous
    def get(self):
        ''' Search for places, calls fs API and yelp API asynchronously
        '''
        self.responses = []
        self.urls_length = 0
        lat = self.get_argument("lat", None)
        lon = self.get_argument("lon", None)
        
        urls = api_search_urls.make(lat=lat, lon=lon)
        self.urls_length = len(urls)
        
        ### Prepare async client
        http = tornado.httpclient.AsyncHTTPClient()

        ### Queue up page fetches
        for url in urls:
            http.fetch(url,
                       callback=self.async_callback(self.on_response))

    @tornado.web.asynchronous
    def on_response(self, response):
        """Callback for get handler. It collects all the responses and writes
        to the client once every page fetch is complete.
        """
        client_callback = self.get_argument("callback", None)
        
        if response.error:
            raise tornado.web.HTTPError(500)
        
        # Decode json, append response list
        json_response = tornado.escape.json_decode(response.body)
        self.responses.append(json_response)
        
        if len(self.responses) == self.urls_length: # All responses have been fetched
            # Clean and merge results
            merged = api_responses.clean(self.responses)
            
            # Format results and write
            resp = {
                'data': merged
            }
            if client_callback:
                resp_str = str(client_callback) + '(' + json.dumps(resp) + ');'
                self.write(resp_str)
                self.finish()
            else:
                self.write(resp)
                self.finish()
    
    def post(self):
        ''' Add a new place or review a place depending on whether place_id is passed
        '''
        request_keys = self.request.arguments.keys()
        # review an existing place if place_id exists
        if Place.A_PLACE_ID in request_keys:
            resp = self.post_review()
        
        # add a new place if place_id does not exist but either yelp_id or fs_id exists
        elif Place.A_FS_ID in request_keys or Place.A_YELP_ID in request_keys:
            resp = self.post_place()
            
        else:
            resp = {'Error': 'Could not complete post'}
        
        self.write(resp)
        self.finish()
    
    def post_review(self):
        place_id = self.get_argument(Place.A_PLACE_ID, None)
        wifi = self.get_argument(Place.A_WIFI, None)
        plugs = self.get_argument(Place.A_PLUGS, None)
        exp = self.get_argument(Place.A_EXP, None)
        
        return place_handler.review_place(place_id=place_id, wifi=wifi, plugs=plugs, exp=exp)
      
    def post_place(self):
        fs_id = self.get_argument(Place.A_FS_ID, None)
        yelp_id = self.get_argument(Place.A_YELP_ID, None)
        name = self.get_argument(Place.A_NAME, None)
        phone = self.get_argument(Place.A_PHONE, None)
        lat = self.get_argument(Place.A_LAT, None)
        lon = self.get_argument(Place.A_LON, None)
        address = self.get_argument(Place.A_ADDRESS, None)
        wifi = self.get_argument(Place.A_WIFI, None)
        plugs = self.get_argument(Place.A_PLUGS, None)
        exp = self.get_argument(Place.A_EXP, None)
        
        resp =  place_handler.add_place(fs_id=fs_id, yelp_id=yelp_id, name=name, phone=phone,
                                        lat=lat, lon=lon, address=address,
                                        wifi=wifi, plugs=plugs, exp=exp)
        return resp
  

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/templates/cofi.html")
        
settings = {
    'debug': True, # enables automatic reruning of this file when edited
    'static_path': os.path.join(os.path.dirname(__file__), "static")
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/places.*", PlacesHandler)
    ],  
     **settings)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()
    

