#
# def questionify(lines):
#     # with open('text.txt', 'r') as file:
#     lines = lines
#
#     drop_str = ['ATTEMPT ALL QUESTIONS IN BRIEF.', 'ATTEMPT ANY THREE OF THE FOLLOWING:',
#                 'ATTEMPT ANY ONE PART OF THE FOLLOWING:',
#                 'ATTEMPT ALL QUESTIONS IN BRIEF:', 'ATTEMPT ANY THREE OF THE FOLLOWING.',
#                 'ATTEMPT ANY ONE PART OF THE FOLLOWING.',
#                 'ATTEMPT ALL QUESTIONS IN BRIEF', 'ATTEMPT ANY THREE OF THE FOLLOWING',
#                 'ATTEMPT ANY ONE PART OF THE FOLLOWING']
#     words = ['MARKS', 'CO', 'QUESTION', 'NOTE', 'QNO.', 'QNO']
#     question_end = ['.', '?', ',', '!']
#     lines1 = []
#
#     QA, QB, QC, question = [], [], [], ''
#     section_a, section_b, section_c, q_line_start, q_line_end = 0, 0, 0, 0, 0
#     lines_in_q = True
#
#     # lines = file.readlines()
#     for line in lines:
#         line = line.split('\n')[0].upper()
#         if not len(line) < 5:
#             lines1.append(line)
#
#     for w in words: drop_str.append(w)
#
#     lines = []
#     for x in (line for line in lines1 if line not in drop_str):
#         lines.append(x)
#
#     for i, line in enumerate(lines):
#         if line == 'SECTION A': section_a, section_b, section_c = 1, 0, 0
#         if line == 'SECTION B': section_a, section_b, section_c = 0, 1, 0
#         if line == 'SECTION C': section_a, section_b, section_c = 0, 0, 1
#
#         for qe in question_end:
#             if line.endswith(qe):
#                 if lines_in_q: q_line_start = i
#                 q_line_end = i
#
#                 question = lines[q_line_start + 1]
#                 if q_line_start < q_line_end:
#                     for q in range(q_line_end - q_line_start - 1):
#                         q_line_start += 1
#                         question += lines[q_line_start + 1]
#
#                 if section_a: QA.append(question)
#                 if section_b: QB.append(question)
#                 if section_c: QC.append(question)
#
#                 question = ''
#                 lines_in_q = True
#             else:
#                 if lines_in_q:
#                     q_line_start = i
#                     lines_in_q = False
#
#     print(QA)  # miss the first question on every section.
#     print(QB)
#     print(QC)  # for section-c question, leave the first question if answer is not matching.
#
# import os
# txt_file = open(os.path.join(r'C:\Users\Ramstein\Desktop\textract', sem_plus_sub), 'wb')
# txt_file.writelines('')
# txt_file.close()


import json, boto3, os

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def csv_reader(event, context):
    # print(event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    obj = s3.get_object(Bucket=bucket, Key=key)

    rows = obj['Body'].read().split('\n')
    table = dynamodb.Table('batch_data')
    with table.batch_writer() as batch:
        for row in rows:
            # registration_id, name
            batch.put_item(Item={
                'registration_id': row.split(',')[0],
                'name': row.split(',')[1]
            })

    # # TODO implement
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
