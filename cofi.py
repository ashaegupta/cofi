import re

import tornado.httpserver
import tornado.autoreload
import tornado.ioloop
import tornado.web
import simplejson

import search

class CofiHandler(tornado.web.RequestHandler):
    # Search for places
    def get(self):
        
        #TODO CHECK PARAMS
        term = self.get_argument("term") 
        location = self.get_argument("location")
        lat = self.get_argument("lat") 
        lon = self.get_argument("lon")    

        resp = search.do(term=term, location=location, lat=lat, lon=lon)
        self.write(resp)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("This is the homepage")

application = tornado.web.Application([
    (r"/", MainHandler),                 # get() - homepage - link to app
   (r"/cofi/.*", CofiHandler)            # get() 
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
    

