from pymongo import MongoClient
import pprint
from random import randint
import csv

pp = pprint.PrettyPrinter(indent=4)
client = MongoClient("mongodb://localhost:27017")
coll = client['osm']['kharkiv']

def get_counts(field, note):
    print("------------")
    print(note)
    count_hash = [{"$group": {"_id": field,
                                   "count":{"$sum": 1}}},
                       {"$sort": {"count": -1}}]
    results = list(coll.aggregate(count_hash))
    pp.pprint(results)

rand_row = randint(0,coll.count())
rand_rec = coll.find().limit(-1).skip(rand_row).next()
print("------------")
print("Random row:")
pp.pprint(rand_rec)

get_counts('$type', "Counting node types:")

print("------------")
print("Top 10 contributing users:")
user_count_hash = [{"$group": {"_id": "$created.user",
                               "count":{"$sum": 1}}},
                   {"$sort": {"count": -1}}]
users_count = list(coll.aggregate(user_count_hash))
pp.pprint(users_count[1:10])

get_counts('$place', "Places count:")
get_counts('$amenity', "Amenities count:")
