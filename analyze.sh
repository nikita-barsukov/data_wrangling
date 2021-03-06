#!/bin/bash
set -e

#Downloading datasets
#cph
wget 'https://onedrive.live.com/download?cid=DEA0FF33116BE269&resid=DEA0FF33116BE269%219286&authkey=AO9docF2k-1HOo0'  -O map_dumps/map_cph
#kharkiv
wget 'https://onedrive.live.com/download?cid=DEA0FF33116BE269&resid=DEA0FF33116BE269%219284&authkey=AByVLi9LicKao6I' -O map_dumps/map_kharkiv
#sthlm
wget "https://onedrive.live.com/download?cid=DEA0FF33116BE269&resid=DEA0FF33116BE269%219285&authkey=ANS1pw6uJ9R8aPE" -O map_dumps/map_sthlm
echo ""
echo "--------"
echo "Map dumps downloaded"

python3 python/process_map_export.py
echo "OSM dumps converted to JSON"

python3 python/import_to_mongo.py
echo "Data imported to MongoDB"

echo "----------"
echo "Producing summary analysis"
python3 python/summary.py

echo "----------"
echo "Identifying and fixing problems"
python3 python/checks_and_problems.py

echo "Identifying and fixing problems"
python3 python/checks_and_problems.py
python3 python/bad_websites.py
