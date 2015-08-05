from pymongo import MongoClient
import pprint
from random import randint

class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

pp = pprint.PrettyPrinter(indent=4)
client = MongoClient("mongodb://localhost:27017")
coll = client['osm']['kharkiv']

rand_row = randint(0,coll.count())
rand_rec = coll.find().limit(-1).skip(rand_row).next()
print("------------")
print("Random row:")
pp.pprint(rand_rec)

#counting node types
print("------------")
print("Counting node types:")
types_count_hash = [{"$group": {"_id": "$type",
                        "count":{"$sum": 1}}},
            {"$sort": {"count": -1}}]
types_count = list(coll.aggregate(types_count_hash))
pp.pprint(types_count)

#counting users
print("------------")
print("Counting users:")
user_count_hash = [{"$group": {"_id": "$created.user",
                               "count":{"$sum": 1}}},
                   {"$sort": {"count": -1}}]
users_count = list(coll.aggregate(user_count_hash))
print(users_count)



