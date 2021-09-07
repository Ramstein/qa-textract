import pandas as pd, os


######################## specify just these values
sem_plus_sub = '07-css'
txt_file_dir = r'C:\Users\Ramstein\Desktop\textract\s3_upload_test'
txt_file = '07-css.txt'


def quanify():
    df = pd.DataFrame({"Question1": [''],
                       'Question2': [''],
                       'Answer': ['']
                       })
    with open(os.path.join(txt_file_dir, txt_file), 'r') as file:
        lines = file.readlines()

        sub_name = ['DESIGN OF STRUCTURE - III']
        contents = []
        # if a line conatains any of these, remove that
        drop_str = ['QUESTIONS-ANSWERS', 'LONG ANSWER TYPE AND MEDIUM ANSWER TYPE QUESTIONS',
                    'VERY IMPORTANT QUESTIONS', 'FOLLOWING QUESTIONS ARE VERY IMPORTANT. THESE QUESTIONS',
                    'MAY BE ASKED IN YOUR SESSIONALS AS WELL AS', 'UNIVERSITY EXAMINATION',
                    'MARKS', '2 MARKS QUESTIONS', 'QUESTION', 'PART-1', 'PART-2', 'PART-3', 'PART-4', 'PART-5',
                    'PART-6', 'PART-7', 'PART-8', 'PART-9', 'PART-10', 'PART-11', 'PART-12', 'PART-13', 'PART-14',
                    'PART-15', 'PART-16', 'PART-17', 'PART-18',
                    'PART-19', 'PART-20', 'PART-21', 'PART-22', 'PART-23', 'PART-24', 'PART-25', 'PART-26', 'PART-27',
                    'PART-28', 'PART-29', 'PART-30',
                    'AKTU', 'MARKS 01', 'MARKS 02', 'MARKS 05', 'MARKS 10', 'MARKS 15', '2010-11', '2011-12', '2012-13',
                    '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22',
                    '2022-23']
        sem = 'CE-SEM'

        question_end = ['.', '?', ',', '!']
        drop_after_qa_detn = ['QUE ', 'OR', 'ANSWER']  # Leading part of the Que line will also be removed.
        lines1 = []
        que_line_start1, que_line_end1, que_line_start2, que_line_end2, ans_line_start, ans_line_end = 0, 0, 0, 0, 0, 0
        que_found1, que_found2, ans_found = 0, 0, 0
        que_idx1, que_idx2, ans_idx = 0, 0, 0

        for line in lines:
            line = line.split('\n')[0].upper()
            lines1.append(line)

        # appending all the dropping strings to one list
        drop_str.append(sem)
        for w in sub_name: drop_str.append(w)
        for w in contents: drop_str.append(w)

        lines = []
        # removing all the sub-strings
        for line in lines1:
            found = 0
            for sub_str in drop_str:
                if line.find(sub_str) != -1: found = 1
            if found != 1: lines.append(line); found = 0
        lines1 = []

        for i, line in enumerate(lines):
            if line.find('QUE') != -1 or line.find('QVE') != -1:
                que_line_start1 = i
                ans_line_end = i - 1
                que_found1 = 1

            if line.find('OR') != -1 or line == 'OR':
                que_line_end1 = i-1
                que_line_start2 = i
                que_found2 = 1

            if line.find('ANSWER') != -1 or line == 'ANSWER':
                que_line_end2 = i - 1
                ans_line_start = i
                ans_found = 1

            if que_found1 == 1:
                answer = lines[ans_line_start + 1]
                if ans_line_start < ans_line_end:
                    for a in range(ans_line_end - ans_line_start - 1):
                        ans_line_start += 1
                        answer += ' ' + lines[ans_line_start + 1]
                que_found1 = 0
                # Writing to DataFrame
                df.at[ans_idx, 'Answer'] = answer
                ans_idx += 1

            if ans_found == 1:
                question = lines[que_line_start1 + 1]
                if que_line_start1 < que_line_end1:
                    for q in range(que_line_end1 - que_line_start1 - 1):
                        que_line_start1 += 1
                        question += ' ' + lines[que_line_start1 + 1]
                # ans_found = 0 # not set it here
                # Writing to DataFrame
                df.at[que_idx1 +1, 'Question1'] = question
                que_idx1 += 1

            if ans_found == 1:
                question = lines[que_line_start2 + 1]
                if que_line_start2 < que_line_end2:
                    for q in range(que_line_end2 - que_line_start2 - 1):
                        que_line_start2 += 1
                        question += ' ' + lines[que_line_start2 + 1]
                ans_found = 0
                # Writing to DataFrame
                df.at[que_idx2 +1, 'Question2'] = question;que_idx2 += 1

    df = df.drop([0])
    df.to_csv(os.path.join(txt_file_dir, sem_plus_sub)+'.csv', index_label='Id')
    print('QA csv file created: '+os.path.join(txt_file_dir, sem_plus_sub)+'.csv')

    # new_row = pd.DataFrame({"Question1": 'what is magnetic confinement?',
    #                         'Question2': 'Describe magnetic confinement?',
    #                         'Answer': 'sheilding the plasma with magnetic field lines.'
    #                         }, index=[1])
    # df = pd.concat([df, new_row]).reset_index(drop=True)


quanify()


