import requests
url_root = "http://127.0.0.1:80/cofi/"
lat = "40.724925"
lon = "-73.9828847"
url = url_root + "lat=" + lat + "&lon=" + lon
r = requests.get(url)
print r.content




payload = {
"lat":"40.724925",
"lon":"-73.9828847"
}

import search
search.do(lat="40.724925",lon="-73.9828847")