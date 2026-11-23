import pdfplumber, openpyxl

wb = openpyxl.load_workbook(r'output\Template_Mutasi_OCT_OUTPUT_1.xlsx', data_only=True)
ws = wb['Tabel_Mutasi']

with pdfplumber.open('templates/master_page_1.pdf') as pdf:
    chars1 = set(c['text'] for c in pdf.pages[0].chars)
with pdfplumber.open('templates/master_page_intermediate.pdf') as pdf:
    chars_mid = set(c['text'] for c in pdf.pages[0].chars)

all_master_chars = chars1.union(chars_mid)

for r in range(6, ws.max_row):
    d = str(ws.cell(r, 4).value or '')
    missing = [c for c in d if c not in all_master_chars and c != '\n']
    if missing:
        print(f"Row {r} (No {ws.cell(r, 1).value}): missing={missing} in text={repr(d)}")
