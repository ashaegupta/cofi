import requests
import simplejson as json

url_root = 'http://localhost:80/places?'
lat = "40.724925"
lon = "-73.9828847"
url = url_root + "lat=" + lat + "&lon=" + lon
r = requests.get(url)
resp = r.content
resp

''''
http://localhost:80/cofi/places?lat=40.724925&lon=-73.9828847
http://splitmyri.de/cofi/places?lat=40.724925&lon=-73.9828847

'''