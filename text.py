# import boto3
# import json, sys
# from pprint import pprint
#
# # amazon textract
# textract = boto3.client(service_name='textract', region_name='us-east-1')
#
# # amazon s3
# s3 = boto3.resource('s3')
# try:
#     response = textract.detect_document_text(
#         Document={
#             "S3Object": {
#                 "Bucket":"ocr-01",
#                 "Name":'New Doc 2020-03-10 15.32.42_1.jpg'
#             }
#         }
#     )
#     # pprint(response)
#     for item in response["Blocks"]:
#         if item["BlockType"] == "LINE":
#             print(item["Text"])
#     print('')
# except Exception as e:
#     print(e)

import sys

A = [64, 25, 12, 22, 11]

# Traverse through all array elements
for i in range(len(A)):

    # Find the minimum element in remaining
    # unsorted array
    min_idx = i
    for j in range(i + 1, len(A)):
        if A[min_idx] < A[j]:
            min_idx = j

            # Swap the found minimum element with
    # the first element
    A[i], A[min_idx] = A[min_idx], A[i]

# Driver code to test above
print("Sorted array")
for i in range(len(A)):
    if i > 2:
        print("%d" % A[i])