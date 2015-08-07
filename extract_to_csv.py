from pymongo import MongoClient
import pprint
import csv

pp = pprint.PrettyPrinter(indent=4)
client = MongoClient("mongodb://localhost:27017")
coll = client['osm']['kharkiv']

user_count_hash = [{"$group": {"_id": "$created.user",
                               "count":{"$sum": 1}}},
                   {"$sort": {"count": -1}}]
users_count = list(coll.aggregate(user_count_hash))

with open('datasets/users.csv', 'w') as f:  # Just use 'w' mode in 3.x
    dict_writer = csv.DictWriter(f, users_count[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(users_count)

timestamps = list(coll.aggregate([{'$project': {'ts': '$created.timestamp'}}]))

with open('datasets/timestamps.csv', 'w') as f:  # Just use 'w' mode in 3.x
    dict_writer = csv.DictWriter(f, timestamps[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(timestamps)
    