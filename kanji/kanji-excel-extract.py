import openpyxl
wb = openpyxl.load_workbook(filename='kanji_table.xlsx')
ws1 = wb.active

cols = 84
rows = 15
col_start = 2
row_start = 2
output_string = ''

for i in range(cols):
    for j in range(rows):
        this_col = i + col_start
        this_row = j + row_start
        char = ws1.cell(column=this_col, row=this_row).value
        if char is not None:
            output_string += char

with open('kanji-out.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(output_string)