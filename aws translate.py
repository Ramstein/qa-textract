import boto3
import json, sys, time, uuid
from pprint import pprint

# amazon textract
textract = boto3.client(service_name='textract', region_name='us-east-1')

# amazon s3
s3 = boto3.resource('s3')
# Amazon translate
translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)


try:
    response = textract.detect_document_text(
        Document={
            "S3Object": {
                "Bucket":"bucket_name",
                "Name": str(sys.argv[1])
            }
        }
    )
    print('')
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            print("\o33[94m"+ item["Text"] + '\o33[0m')
            result = translate.translate_text(Text=item['Text'],
                                              SourceLangaugeCode='en',
                                              TrargetLanguageCode='de')
            print("\o33[92m"+ result.get('TranslatedText') + '\o33[0m')
            print('')
except Exception as e:
    print(e.message)