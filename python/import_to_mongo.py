from pymongo import MongoClient
import json
import pprint
import codecs
import time

pp = pprint.PrettyPrinter(indent=4)

def insert_data(data, db, coll):
    for d in data:
        d['created']['timestamp_parsed'] = time.strptime(d['created']['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
        db[coll].insert(d)

client = MongoClient("mongodb://localhost:27017")
client.drop_database('osm')
db = client['osm'];

cities = ['kharkiv', 'cph', 'sthlm']

for city in cities:
    print('Importing data for city ' + city)
    fname = 'map_dumps/map_' + city + '.json'
    with codecs.open(fname, 'r',encoding='utf-8') as f:
        data = json.loads(f.read())
        insert_data(data, db, city)
        pp.pprint(db[city].find_one())
