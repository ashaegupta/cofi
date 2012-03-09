import requests
url_root = "http://splitmyri.de/cofi/"

# Search by location
payload = {
    "location":"nyc",
    }
    
r = requests.get(url_root, data=payload)
print r.content