import boto3
import json, sys, time, uuid
from pprint import pprint

# amazon textract
textract = boto3.client(service_name='textract', region_name='us-east-1')

# amazon s3
s3 = boto3.resource('s3')
# Amazon comprehend
comprehend_client = boto3.client(region_name='us-east-1').client('comprehend')
try:
    response = textract.detect_document_text(
        Document={
            "S3Object": {
                "Bucket":"bucket_name",
                "Name": str(sys.argv[1])
            }
        }
    )
    para = ''
    # pprint(response)
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            para = para + '' + item['Text']
        sentiment_analysis = comprehend_client.detect_sentiment(LanguageCode='en', Text=para)
        print("Sentiment: "+sentiment_analysis.get('Sentiment'))
        print('')
except Exception as e:
    print(e.message)