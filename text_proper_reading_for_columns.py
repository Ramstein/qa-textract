import sys

import boto3, json, sys

# amazon textract
textract = boto3.client(service_name='textract', region_name='us-east-1')

# amazon s3
s3 = boto3.resource('s3')

response = textract.detect_document_text(
    Document={
        "S3Object": {
            "Bucket": "bucket_name",
            "Name": str(sys.argv[1])
        }
    }
)

columns = []
lines = []
for item in response["Blocks"]:
    if item['BlockType'] == "LINE":
        column_found = False
        for index, column in enumerate(columns):
            bbox_left = item['Geometry']['BoundingBox']['Left']
            bbox_right = item['Geometry']['BoundingBox']['Left'] + item['Geometry']['BoundingBox']['Width']
            bbox_centre = item['Geometry']['BoundingBox']['Left'] + item['Geometry']['BoundingBox']['Width']
            column_centre = column["left"] + column["right"]

            if (column["left"] < bbox_centre < column['right']) or (
                    bbox_left < column_centre < bbox_right):
                # BBox appears inside the column
                lines.append([index, item['Text']])
                column_found = True
                break
        if not column_found:
            columns.append({'left': item['Geometry']['BoundingBox']['Left'],
                            'right': item['Geometry']['BoundingBox']['Left'] + item['Geometry']['BoundingBox'][
                                'Width']})
            lines.append([len(columns) - 1, item['Text']])


lines.sort(key=lambda x: x[0])
for line in lines:
    print(line[1])
