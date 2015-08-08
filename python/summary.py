from pymongo import MongoClient
import pprint
from random import randint
import csv

pp = pprint.PrettyPrinter(indent=4)
client = MongoClient("mongodb://localhost:27017")
coll_kh = client['osm']['kharkiv']
coll_sthlm = client['osm']['sthlm']
coll_cph = client['osm']['cph']

def get_counts(field, note, col):
    print("------------")
    print(note)
    count_hash = [{"$group": {"_id": field,
                                   "count":{"$sum": 1}}},
                       {"$sort": {"count": -1}}]
    results = list(col.aggregate(count_hash))
    return(results)

pp.pprint(get_counts('$type', "Counting node types:", coll_kh))

print("------------")
print("Top 10 contributing users:")
user_count_hash = [{"$group": {"_id": "$created.user",
                               "count":{"$sum": 1}}},
                   {"$sort": {"count": -1}}]
users_count = list(coll_kh.aggregate(user_count_hash))
pp.pprint(users_count[1:10])
print('Unique users: ' + str(len(users_count)))


pp.pprint(get_counts('$place', "Places count:", coll_kh))
amn_kh = get_counts('$amenity', "Amenities count, Kharkiv:", coll_kh)
pp.pprint(amn_kh)
amn_sthlm = get_counts('$amenity', "Amenities count, Stockholm:", coll_sthlm)
pp.pprint(amn_sthlm[1:10])
amn_cph = get_counts('$amenity', "Amenities count, Copenhagen:", coll_cph)
pp.pprint(amn_cph[1:10])
print('Amenity types Kharkiv: ' + str(len(amn_kh)))
