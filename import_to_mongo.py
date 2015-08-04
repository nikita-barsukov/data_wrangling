from pymongo import MongoClient
import json
import codecs

def insert_data(data, db):
    for d in data:
        db.kharkiv.insert(d)

client = MongoClient("mongodb://localhost:27017")
db = client['osm']

with codecs.open('map.json', 'r',encoding='utf-8') as f:
    data = json.loads(f.read())
    insert_data(data, db)
    print(db.kharkiv.find_one())