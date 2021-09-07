import pandas as pd
from fuzzywuzzy import process


lines = []

s3_files = []
# amazon s3
# s3 = boto3.resource('s3')
# for s3_file in s3_files:
#     try:
#         response = textract.detect_document_text(
#             Document={
#                 "S3Object": {
#                     "Bucket":bucket_name,
#                     "Name":s3_file
#                 }
#             }
#         )
#         for item in response["Blocks"]:
#             if item["BlockType"] == "LINE":
#                 lines.append(item["Text"])
#     except Exception as e:
#         print(e)

# qa, qb, qc = questionify(lines)


qa = ['SECTION A 2 X 7 - 14 A) ENLIST DIFFERENT TYPES OF SENSORS INCORPORATED IN A ROBOT.', 'B) DEFINE AUTOMATION.',
      'C) DIFFERENTIATE BETWEEN AUTOMATION AND ROBOTICS.', 'D) WHAT IS MEANT BY ACCURACY OF A ROBOT?',
      'E) WHAT ARE THE CHARACTERISTICS OF A SERVOMOTOR?',
      'F) EXPLAIN THE FUNCTIONS OF A HYDRAULIC FLUID G) EXPLAIN THE WORKING OF AN ELECTROMAGNETIC RELAY.']
qb = [
    'SECTION B 7 X 3 = 21 A) DISCUSS IN DETAIL THE INTEGRATION OF MECHANICAT "SYSTEMS WITH ELECTRONICS AND COMPUTER SYSTEM.',
    'B) IDENTIFY THE VARIOUS TYPES OF TRANSFER DEY DERIEI USED IN INDUSTRIAL AUTOMATION. EXPLAIN THE WORKING OF ANY TWO TRANSFER DEVICES WITH THE HELP OF NEAT SHETCHES.',
    'C) A ROBOT IS TO BE USED FOR SPOT WELDING INT AN AUTOMOTIVE INDUSTRY FOR SPOT WELDING OF CAR BODY SELECT THE ROOT TO BE USED AND EXPLAIN THE GEOMETRY, CONTROL STRATEGY, TYPE OF DRIVE OF THE SELECTED ROBOTS D) ENLIST THE LAWS OF ROBOTICS DISCUSS VARIOUS TYPES OF ROBOTS IN DETAIL ALONG WITH THEIR APPLICATIONS E) EXPLAIN THE VARIOUS DRIVE SYSTEMS FOR ROBOT END EFFECTORS. HOW ARE GRIPPERS CLASSIFIED? EXPLAIN ANY ONE OF THEM.']
qc = [
    'SECTION C 7X1-7 1 A) DISCUSS THE ROLE OF PLC IN AUTOMATIOU AND ROBOTICS. ENLIST AND EXPLAIN VARIOUS ELEMENTS OF AUTOMATION.']

df = pd.read_csv(r'C:\Users\Ramstein\Desktop\textract\qa.csv')
# df.head()

n_char_in_A_ans = 250
n_char_in_B_ans = 1250
n_char_in_C_ans = 1250

Question1_list = list(df['Question1'])
Question2_list = list(df['Question2'])

A_ans, B_ans, C_ans = [], [], []
best, best1, best2 = [], [], []

############################### section-A question answer formatting
for i, que in enumerate(qa):
    best1.append(process.extractOne(que, Question1_list))
    best2.append(process.extractOne(que, Question2_list))

    if best1[i][1] > best2[i][1]:
        for j, que in enumerate(Question1_list):
            if que == best1[i][0]:
                A_ans.append([que, str(df.at[j, 'Answer'])[:n_char_in_A_ans]])
                break
    else:
        for j, que in enumerate(Question2_list):
            if que == best2[i][0]:
                A_ans.append([que, str(df.at[j, 'Answer'])[:n_char_in_A_ans]])
                break
del qa, j, n_char_in_A_ans
################################ section-B question answer formatting

best, best1, best2 = [], [], []
best1_similar, best2_similar = [], []

for i, que in enumerate(qb):
    best1.append(process.extractOne(que, Question1_list))
    best2.append(process.extractOne(que, Question2_list))

    if best1[i][1] > best2[i][1]:
        best1_similar.append(best1[i])
    else:
        best2_similar.append(best2[i])

del qb
best1, best2 = [], []

for best2_s in best2_similar: best1_similar.append(best2_s)

# sorting the questions in descending form of duplication
for i in range(len(best1_similar)):
    min_idx = 1
    for j in range(i + 1, len(best1_similar)):
        if best1_similar[min_idx][1] < best1_similar[j][1]:
            min_idx = j
    best1_similar[i], best1_similar[min_idx] = best1_similar[min_idx], best1_similar[i]

for i, best1_s in enumerate(best1_similar):
    if i > 2: break
    found = 0
    for j, que in enumerate(Question1_list):
        if que == best1_s:
            B_ans.append([best1_s[0], str(df.at[j, 'Answer'])[:n_char_in_B_ans]])
            found = 1
            break
        if found != 1:
            for j, que in enumerate(Question2_list):
                if que == best1_s:
                    B_ans.append([best1_s[0], str(df.at[j, 'Answer'])[:n_char_in_B_ans]])
                    break

del best1_s, n_char_in_B_ans

######################## section-C question answer formatting
best, best1_1, best2_2 = [], [], []
best_similar, best1_similar, best2_similar = [], [], []

for i, que in enumerate(qc):
    if i % 2 == 0:
        best1.append(process.extractOne(que, Question1_list))
        best2.append(process.extractOne(que, Question2_list))
        continue
    if i % 2 != 0:
        best1_1.append(process.extractOne(que, Question1_list))
        best2_2.append(process.extractOne(que, Question2_list))

        if best1[i - 1][1] > best2[i - 1][1]:
            best1_similar.append(best1[i - 1])
        else:
            best2_similar.append(best2[i - 1])

        if best1_1[i][1] > best2_2[i][1]:
            best2_similar.append(best1_1[i])
        else:
            best2_similar.append(best2_2[i])

        if best1_similar[i - 1][1] > best2_similar[i][1]:
            best_similar.append(best1_similar[i - 1])
        else:
            best_similar.append(best2_similar[i])

# garbage collection
del best1_similar, best2_similar, best, best1, best2, best1_1, best2_2

for i, best_s in enumerate(best_similar):
    found = 0
    for j, que in enumerate(Question1_list):
        if que == best_s:
            C_ans.append([best_s[0], str(df.at[j, 'Answer'])[:n_char_in_C_ans]])
            found = 1
            break
    if found != 1:
        for j, que in enumerate(Question2_list):
            if que == best_s:
                C_ans.append([best_s[0], str(df.at[j, 'Answer'])[:n_char_in_C_ans]])
                break

# garbage collection
del best_similar, df, que, Question1_list, Question2_list, n_char_in_C_ans


section_text = ['']
with open('log.txt', 'w') as f:
    for i in A_ans:
        f.write('Section A Question                    ' + i[0] + ' Answer.                     ' + i[1] + '                    ')
    del A_ans
    for i in B_ans:
        f.write('Section B Question                    ' + i[0] + ' Answer.                     ' + i[1] + '                    ')
    del B_ans
    for i in C_ans:
        f.write('Section C Question                    ' + i[0] + ' Answer.                     ' + i[1] + '                    ')
    del C_ans

