def get_sentiment(text):
  import boto3
  import json

  comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
  response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
  return response["Sentiment"]
