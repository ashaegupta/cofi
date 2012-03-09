import requests


url_root = "http://splitmyri.de/cofi/"

# Search by location
payload = {
    "term":"",
    "location":"nyc",
    "lat":"",
    "lon":""
    }
r = requests.get(url_root, data=payload)
print r.text