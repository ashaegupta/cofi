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

from lib import api_search_urls
from lib import api_responses

class PlacesHandler(tornado.web.RequestHandler):
    # Search for places, calls fs API and yelp API asynchronously
    @tornado.web.asynchronous
    def get(self):
        self.responses = list()
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
    

