#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import re
import codecs
import json

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        node['id'] = element.attrib['id']
        node['type'] = element.tag
        if element.find('nd') is not None:
            for t in element.findall('nd'):
               node.setdefault('node_refs', [])
               node['node_refs'].append(t.attrib['ref'])
                
        if element.find('tag') is not None:
            for t in element.findall('tag'):
                if 'addr' in t.attrib['k']:
                    spl = t.attrib['k'].split(":")
                    if len(spl) > 2:
                        continue
                    else:
                        node.setdefault('address', {})
                        node['address'][spl[1]] = t.attrib['v']
                else:
                    node[t.attrib['k']] =  t.attrib['v']
                        
        if 'visible' in element.attrib:
            node['visible'] = element.attrib['visible']
        if 'lat' in element.attrib:
            node['pos'] = [float(element.attrib['lat']),float(element.attrib['lon']) ]
        for tag in CREATED:
            if tag in element.attrib:
                node.setdefault('created', {})
                node['created'][tag] = element.attrib[tag]
                
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w", encoding='utf-8') as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
        fo.write(json.dumps(data , indent=2, ensure_ascii=False)+"\n")
    return data

data = process_map('map_dumps/map_kharkiv', True)

