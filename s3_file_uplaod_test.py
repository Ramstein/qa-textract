import logging

import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError
from tqdm import tqdm

sem_plus_sub = '07-css'  # no capital, no underscore
file_dir = r'C:\Users\Ramstein\Desktop\textract\s3_upload_test'

bucket_name = sem_plus_sub + 'textract-upload'
# bucket_name = 'ocr-01'
region = 'eu-west-1'

# ACCESS_KEY = 'AKIARYVRQMD6V2NV4DJC'
# SECRET_KEY = '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'

files = os.listdir(file_dir)
s3_client = boto3.client('s3')


def create_bucket(bucket_name, s3_client, region=None):
    # if Bucket is already owned, it will move forward.
    try:
        if region is None:
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_to_aws(local_file, bucket, s3_file_name):
    try:
        s3_client.upload_file(local_file, bucket, s3_file_name)
        return True
    except FileNotFoundError:
        print("File not found: " + local_file)
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


if create_bucket(bucket_name, s3_client, region=region): print('Bucket:' + bucket_name + 'created.')
for file in tqdm(files):
    local_file = os.path.join(file_dir, file)
    s3_file_name = file

    upload_to_aws(local_file, bucket_name, s3_file_name)

lines = []
# amazon s3
s3 = boto3.resource('s3')

# amazon textract
textract = boto3.client(service_name='textract', region_name=region)

txt_file = open(os.path.join(file_dir, sem_plus_sub) + '.txt', 'w')

for file in tqdm(files):
    try:
        response = textract.detect_document_text(
            Document={
                "S3Object": {
                    "Bucket": bucket_name,
                    "Name": file
                }
            }
        )
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                #                 lines.append(item["Text"])
                #                 print(item["Text"])
                txt_file.write(item["Text"] + '\n')

    except Exception as e:
        print(e)

txt_file.close()
