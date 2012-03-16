import requests
url_root = "http://splitmyri.de/cofi/places"
lat = "40.724925"
lon = "-73.9828847"
url = url_root + "lat=" + lat + "&lon=" + lon
r = requests.get(url)
print r.content


import requests
import simplejson as json
url_root = 'http://localhost:80/cofi/places?'
lat = "40.724925"
lon = "-73.9828847"
url = url_root + "lat=" + lat + "&lon=" + lon

r = requests.get(url)
resp = r.content
resp

''''
http://splitmyri.de/cofi?lat=40.724925&lon=-73.9828847

'''