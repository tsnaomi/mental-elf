#!/bin/bash

URL=$( python crawl_test.py --disorder $2 )
python scraper.py --id $1 --overview_url $URL --output_file tmp.json
aws dynamodb put-item --table-name Conditions --item file://tmp.json
rm tmp.json
