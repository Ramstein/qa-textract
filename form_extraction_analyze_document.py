import re
import sys

import boto3

file_name = sys.argv[1]
# amazon textract
textract = boto3.client(service_name='textract', region_name='us-east-1',
                        endpoint_url='https://textract.us-east-1.amazonaws.com')

# amazon s3
s3 = boto3.resource('s3')


def get_kv_map(filename):
    # with open(file_name, 'rb') as file:
    #     img_test = file.read()
    #     bytes_test = bytearray(img_test)
    #     print('Image loaded', file_name)
    # process using iamge bytes
    # response = textract.analyze_document(Document={'Bytes': bytes_test},
    #                                      FeatureTypes=['FORMS'])
    response = textract.analyze_document(
        Document={
            "S3Object": {
                "Bucket":"ocr-01",
                "Name":'IMG_20200310_110946.jpg'
            }
        }, FeatureTypes=['TABLES']
    )


    # get the text block
    blocks = response["Blocks"]
    # print(blocks)
    # get key and value maps
    key_map = {}
    value_map = {}
    block_map = {}
    for block in blocks:
        block_id = block['Id']
        block_map[block_id] = block
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'KEY' in block['EntityTypes']:
                key_map[block_id] = block
            else:
                value_map[block_id] = block
    return key_map, value_map, block_map


def get_kv_relationship(key_map, value_map, block_map):
    kvs = {}
    for block_id, key_block in key_map.items():
        value_block = find_value_block(key_block, value_map)
        key = get_text(key_block, block_map)
        val = get_text(value_block, block_map)
        kvs[key] = val
    return kvs


def find_value_block(key_block, value_map):
    for relationship in key_block['Relationship']:
        if relationship['Type'] == "VALUE":
            for value_id in relationship['Ids']:
                value_block = value_map[value_id]
    return value_block


def get_text(result, blocks_map):
    text = ''
    if 'Relationship' in result:
        for relationship in result['Relationship']:
            if relationship['Type'] == "CHILD":
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == "WORD":
                        text += word['Text'] + ' '
    return text


def print_kvs(kvs):
    for key, value in kvs.items():
        print(key, ":", value)


def search_value(kvs, search_key):
    for key, value in kvs.items():
        if re.search(search_key, key, re.IGNORECASE):
            return value


# MAIN PROGRAM
key_map, value_map, block_map = get_kv_map(file_name)

# Get key value relationship
kvs = get_kv_relationship(key_map, value_map, block_map)
print("\n\n== FOUND KEY : VALUE Pairs ===\n")
print_kvs(kvs)

# start searching a key value
while input('\n Do you want to search a value for a key? (enter "n" for exit) ' != 'n'):
    search_key = input('\n Enter a search key: ')
    print('The value is: ', search_value(kvs, search_key))
