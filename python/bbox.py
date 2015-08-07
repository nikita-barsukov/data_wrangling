from pymongo import MongoClient
import pprint
import math

pp = pprint.PrettyPrinter(indent=4)
client = MongoClient("mongodb://localhost:27017")
coll = client['osm']['kharkiv']

def bbox(col):
    grp_hash = {'$group': {
                '_id': None,
                'min': {'$min' : "$coords"},
                'max': {'$max' : "$coords"}         
            }}
    lats = coll.aggregate([
            {'$project': {'coords': {'$slice': ['$pos', 1]}}},
            {'$unwind': '$coords'},
            grp_hash
        ])
    longs = coll.aggregate([
            {'$project': {'coords': {'$slice': ['$pos', 1, 1]}}},
            {'$unwind': '$coords'},
            grp_hash
        ])
    return([list(lats)[0], list(longs)[0]])

def bbox_area(bbox):
    R = 6371
    lat_max_rad = math.radians(bbox[0]['max'])
    lat_min_rad = math.radians(bbox[0]['min'])
    sq = R**2 * math.pi * (math.sin(lat_max_rad) - math.sin(lat_min_rad)) * (bbox[1]['max'] - bbox[1]['min'])/180   
    return(sq)

b = bbox(coll)
print('Bounding box, Kharkiv: ')
print(b)
print('Number of documents: ')
print(coll.count())
