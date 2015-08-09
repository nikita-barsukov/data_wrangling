from pymongo import MongoClient
import requests

client = MongoClient("mongodb://localhost:27017")
coll_kh = client['osm']['kharkiv']

print("Documents with given website: ", coll_kh.count({'website': {'$exists': True}}))
websites = list(coll_kh.find({'website': {'$exists': True}}, {'website': 1, 'name': 1}))

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
        rec = coll_kh.find_one({'_id': site['_id']})
        del(rec['website'])
        coll_kh.save(rec)
        print('Website deleted')
        continue
