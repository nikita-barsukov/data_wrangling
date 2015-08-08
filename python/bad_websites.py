from pymongo import MongoClient
import requests

client = MongoClient("mongodb://localhost:27017")
coll_kh = client['osm']['kharkiv']

print("Documents with given website: ", coll_kh.count({'website': {'$exists': True}}))
websites = list(coll_kh.find({'website': {'$exists': True}}, {'website': 1, 'name': 1, '_id': 0}))

for site in websites:
    url = site['website']
    if 'http://' not in url:
        if 'https://' in url: 
            url = site['website']
        else:
            url = 'http://' + url
    try:
        r = requests.get(url)
    except:
        print(url, ' connection error')
        continue
