import boto3
import json

def get_sentiment(text):

  comprehend = boto3.client(service_name='comprehend', region_name='us-west-2')
  response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
  print(response)
  return response["Sentiment"].lower()
