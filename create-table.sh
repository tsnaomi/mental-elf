#!/bin/bash

aws dynamodb create-table \
  --table-name Conditions \
  --attribute-definitions \
    AttributeName=Condition,AttributeType=S \
    AttributeName=Id,AttributeType=N \
  --key-schema \
    AttributeName=Condition,KeyType=HASH \
    AttributeName=Id,KeyType=RANGE \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

