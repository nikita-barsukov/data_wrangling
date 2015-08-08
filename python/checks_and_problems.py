from pymongo import MongoClient
import pprint
from collections import Counter
import requests

pp = pprint.PrettyPrinter(indent=4)
client = MongoClient("mongodb://localhost:27017")
coll_kh = client['osm']['kharkiv']
coll_sthlm = client['osm']['sthlm']
coll_cph = client['osm']['cph']
#
#counts
print('Stockholm data ' + str(coll_sthlm.count()))
print('Copenhagen data ' + str(coll_cph.count()))
print('Kharkiv data ' + str(coll_kh.count()))

def get_addr_sanity_check(col):
    addresses = col.aggregate([
                {'$match': {'address': {'$exists': True},
                            'name': {'$exists': True}}},
                {'$project': {
                    'name': '$name',
                    'addr': '$address',
                    '_id': 0
                }}
            ])
    addresses = list(addresses)
    addr_counts = list(map(lambda x: {'addr_size': str(len(x['addr'])), 'name': x['name']}, addresses))
    simple_counts= list(map(lambda x: str(len(x['addr'])), addresses))
    return(dict(Counter(simple_counts)))

print('Checking addresses KHR')
pp.pprint(get_addr_sanity_check(coll_kh))
print('Checking addresses Stockholm')
pp.pprint(get_addr_sanity_check(coll_sthlm))

no_eng = coll_kh.count({'name': {'$exists': True},
                        'name:en': {'$exists': False}})
no_ru = coll_kh.count({'name': {'$exists': True},
                        'name:ru': {'$exists': False}})
total_name = coll_kh.count({'name': {'$exists': True}})

print("Total elements with name:", total_name)
print("Nodes with no English translation", no_eng)
print("Nodes with no Russian translation", no_ru)

