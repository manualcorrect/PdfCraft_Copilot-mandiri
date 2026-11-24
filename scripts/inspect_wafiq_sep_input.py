import pdfplumber, openpyxl, os

base_sep = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep'
pdf_path = os.path.join(base_sep, '0.pdf')
excel_path = os.path.join(base_sep, 'Template_Mutasi_SEP.xlsx')

print("=== 0.PDF (WAFIQ SEP) ===")
with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    for p_idx in range(len(pdf.pages)):
        p = pdf.pages[p_idx]
        wibs = [w for w in p.extract_words() if w['text'] == 'WIB']
        print(f"Page {p_idx+1}: {len(wibs)} transactions")
    
    p1 = pdf.pages[0]
    words = p1.extract_words()
    print("\n--- Page 1 Header Words ---")
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        if w['top'] < 160:
            print(f"{w['top']:.2f}, {w['x0']:.2f}: {w['text']}")

print("\n=== TEMPLATE_MUTASI_SEP.XLSX ===")
wb = openpyxl.load_workbook(excel_path)
print("Sheet names:", wb.sheetnames)
ws_hr = wb['Header & Ringkasan']
for r in range(1, 30):
    val_a = ws_hr.cell(r, 1).value
    val_b = ws_hr.cell(r, 2).value
    if val_a or val_b:
        print(f"A{r}: {val_a} | B{r}: {val_b}")

ws_tm = wb['Tabel_Mutasi']
print(f"\nTabel_Mutasi max_row: {ws_tm.max_row}")
for r in range(1, 20):
    vals = [ws_tm.cell(r, c).value for c in range(1, 9)]
    if any(vals):
        print(f"Row {r:2d}: {vals}")
