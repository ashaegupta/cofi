import os
import re
import tornado.httpserver
import tornado.autoreload
import tornado.ioloop
import tornado.web
import simplejson as json

from lib import search

class CofiPlacesHandler(tornado.web.RequestHandler):
    # Search for places
    def get(self):
        term = self.get_argument("term", None)
        lat = self.get_argument("lat", None)
        lon = self.get_argument("lon", None)
        callback = self.get_argument("callback", None)
        
        resp = search.do(term=term, lat=lat, lon=lon)
        if callback:
            resp_str = str(callback) + '(' + json.dumps(resp) + ');'
            self.write(resp_str)
        else:
            self.write(resp)

class CofiHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/templates/cofi.html")
    
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("This is the homepage")

settings = {
    'debug': True, # enables automatic reruning of this file when edited
    'static_path': os.path.join(os.path.dirname(__file__), "static")
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/cofi.*", CofiHandler),                    
    (r"/cofi/places.*", CofiPlacesHandler)              
    ],  
     **settings)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
    

