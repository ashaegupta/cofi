import requests
url_root = "http://127.0.0.1:80/cofi/"
payload = {
"lat":"40.724925",
"lon":"-73.9828847"
}
r = requests.get(url_root, data=payload)
print r.content


import search
search.do(lat="40.724925",lon="-73.9828847")