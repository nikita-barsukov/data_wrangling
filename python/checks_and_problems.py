from pymongo import MongoClient
import pprint
from collections import Counter
import requests
import re

pp = pprint.PrettyPrinter(indent=4)
client = MongoClient("mongodb://localhost:27017")
coll_kh = client['osm']['kharkiv']
coll_sthlm = client['osm']['sthlm']
coll_cph = client['osm']['cph']


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

def get_distinct_addr_fields(col, addr_field):
    f = 'address.' + addr_field
    address_fields = col.aggregate([
                {'$match': {f: {'$exists': True}}},
                {'$group': {
                    '_id': '$'+f,
                    "count":{"$sum": 1}
                }}
        ]) 
    return(list(address_fields))   

print('Checking addresses KHR')
print('---Number of address fields:')
pp.pprint(get_addr_sanity_check(coll_kh))
postcode_counts = get_distinct_addr_fields(coll_kh, 'postcode')
postcode_lengths = list(map(lambda x: str(len(x['_id'])), postcode_counts))
print('---Postcode lengths')
pp.pprint(dict(Counter(postcode_lengths)))
print('---Last words in streetnames')
street_names_counts = get_distinct_addr_fields(coll_kh, 'street')
last_words = map(lambda x: x['_id'].split()[-1], street_names_counts)
pp.pprint(dict(Counter(list(last_words))))
print('---Fixing street names')
regx = re.compile("^вулиця", re.IGNORECASE)
bad_steet_names = coll_kh.find({'address.street': regx})
for str_name in bad_steet_names:
    record = coll_kh.find_one({'_id': str_name['_id']})
    s = record['address']['street']
    s = s.replace('вулиця ', '')
    s = s + ' вулиця'
    record['address']['street'] = s
    coll_kh.save(record)
print('---FIXED')

print('---Fixing translations')
bad_translations = coll_kh.find({'address.street': 'Рынок Барабашово'})
for str_name in bad_translations:
    record = coll_kh.find_one({'_id': str_name['_id']})
    record['address']['street'] = 'Ринок Барабашова'
    coll_kh.save(record)
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

