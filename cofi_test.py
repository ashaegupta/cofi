import requests
url_root = "http://splitmyri.de/cofi/"
lat = "40.724925"
lon = "-73.9828847"
url = url_root + "lat=" + lat + "&lon=" + lon
r = requests.get(url)
print r.content


import requests
import simplejson as json
url_root = "http://splitmyri.de/cofi/"
payload = { "lat":"40.724925", "lon":"-73.9828847" }
r = requests.get(url_root, data=json.dumps(payload))
print r.content


import search
search.do(lat="40.724925",lon="-73.9828847")