import re
import tornado.httpserver
import tornado.autoreload
import tornado.ioloop
import tornado.web
import simplejson as json

import search

class CofiHandler(tornado.web.RequestHandler):
    # Search for places
    def get(self):
        term = self.get_argument("term", None)
        lat = self.get_argument("lat", None)
        lon = self.get_argument("lon", None)
        print self.request.arguments
        resp = search.do(term=term, lat=lat, lon=lon)
        self.write(json.dumps(resp))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("This is the homepage")

app_settings = {
    'debug': True
}

application = tornado.web.Application([
    (r"/", MainHandler),                    # get() - homepage - link to app
    (r"/cofi.*", CofiHandler)              # get() - places 
    ],  
     **app_settings)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
    

