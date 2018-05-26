#!/bin/bash

# getting and deleting last id
ID=$( python make_id.py $( aws dynamodb scan --table-name Number_Conditions ) )
python make_number_conditions_key.py $ID
aws dynamodb delete-item --table-name Number_Conditions --key file://tmp.json
rm tmp.json

# putting in new id
ID=$(( $ID + 1 ))
python make_number_conditions_key.py $ID
aws dynamodb put-item --table-name Number_Conditions --item file://tmp.json
rm tmp.json

# putting in new item
URL=$( python crawl_test.py --disorder $1 )
python scraper.py --id $ID --overview_url $URL --output_file tmp.json
aws dynamodb put-item --table-name Conditions --item file://tmp.json
rm tmp.json
