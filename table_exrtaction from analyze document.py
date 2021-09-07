import sys
import webbrowser

import boto3
import os

file_name = r'C:\Users\Ramstein\Desktop\Camera\IMG_20200310_110946.jpg'
# amazon textract
textract = boto3.client(service_name='textract', region_name='us-east-1')

# amazon s3
s3 = boto3.resource('s3')


def get_table_html_results(file_name):
    with open(file_name, "rb") as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        print("Image Loaded.", file_name)

    # Process using image bytes
    response = textract.analyze_document(Document={'Bytes': bytes_test},
                                         FeatureTypes=['TABLES'])
    # get the text block
    blocks = response["Blocks"]
    # print(blocks)

    blocks_map = {}
    table_blocks = []
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == 'TABLE':
            table_blocks.append(block)

    if len(table_blocks) <= 0:
        return "<b> No table found </b>"
    html = ' '
    for index, table in enumerate(table_blocks):
        html += generate_table_html(table, blocks_map, index + 1)
        html += "<hr>\n\n"
    return html


def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationship']:
        if relationship['Type'] == "CHILD":
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == "CELL":
                    row_index = cell["RowIndex"]
                    col_index = cell["columnIndex"]
                    if row_index not in rows:
                        rows[row_index] = {}  # create new row
                    # get the text value
                    rows[row_index][col_index] = get_text(cell, blocks_map)
    return rows


def get_text(result, blocks_map):
    text = ' '
    if 'Relationship' in result:
        for relationship in result['Relationship']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word["Text"] + ' '
    return text


def generate_table_html(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)

    is_first_table = True if table_index == 1 else False
    table_id = "Table_" + str(table_index)
    # get cells
    area_expanded = 'true' if is_first_table else False
    collapse_show = 'show' if is_first_table else ' '
    table_html = '<div class="card"><div class=card-reader" id="headingOne">' \
                 '<h5 class="mb-0">' \
                 '<button class="btn btn-link" data-toggle="collapse" data-target="#{}" ' \
                 'aria-expanded="{}" aria-controls="collapseOne">{}</button>' \
                 '</h5>' \
                 '</div>'.format(table_id, area_expanded, table_id)
    table_html += '<div id="{}" class="collapse {}" data-parent="#accordion">' \
                  '<div class="card-body">' \
                  '<table class="myTable table table-hover">\n'.format(table_id, collapse_show)

    for row_index, cols in rows.items():
        table_html += '<tr row="{}">\n'.format(row_index)

        for col_index, text in cols.items():
            table_html += '<td col="{}"> {} </td>\n'.format(col_index, text)
        table_html += '<tr>\n'

    table_html += '</table> </div> </div></div>\n'
    return table_html


table_html = get_table_html_results(file_name=file_name)

tempalte_file = 'template.html'
output_file = 'output.html'

# replace content
with open(tempalte_file, 'rt') as fin:
    with open(output_file, "wt") as fout:
        for line in fin:
            fout.write(line.replace('[[REPLACE_TITLE]]', 'Table results for ' + file_name)
                       .replace('[[REPLACE_TITLE]]', table_html))

# show the results
webbrowser.open('file://' + os.path.realpath(output_file))
