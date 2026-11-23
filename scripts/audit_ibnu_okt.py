import pdfplumber
import openpyxl
import re

okt_dir = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\okt"
pdf_path = f"{okt_dir}\\0.pdf"
xlsx_path = f"{okt_dir}\\Template_Mutasi_OKT.xlsx"

print("==================================================")
print("AUDIT IBNU AGUN - OKTOBER 2026")
print("==================================================")

# 1. Audit Excel
wb = openpyxl.load_workbook(xlsx_path, data_only=True)
print("Excel Sheets:", wb.sheetnames)

ws_hr = wb["Header & Ringkasan"] if "Header & Ringkasan" in wb.sheetnames else None
if ws_hr:
    print("Header & Ringkasan values:")
    for r in range(1, 30):
        a_val = ws_hr[f'A{r}'].value
        b_val = ws_hr[f'B{r}'].value
        if a_val is not None or b_val is not None:
            print(f"  A{r}: {a_val} | B{r}: {b_val}")

ws1 = wb["Sheet1"] if "Sheet1" in wb.sheetnames else wb.active
excel_rows = []
for r in range(6, ws1.max_row + 1):
    c_no = ws1.cell(r, 1).value
    c_date = ws1.cell(r, 2).value
    c_desc = ws1.cell(r, 3).value
    c_kredit = ws1.cell(r, 4).value
    c_debit = ws1.cell(r, 5).value
    c_saldo = ws1.cell(r, 6).value
    
    # Check if empty row
    if c_no is None and c_date is None and c_desc is None and c_kredit is None and c_debit is None:
        continue
    
    excel_rows.append({
        'row': r,
        'no': c_no,
        'date': c_date,
        'desc': str(c_desc or '').strip(),
        'kredit': c_kredit or 0,
        'debit': c_debit or 0,
        'saldo': c_saldo
    })

print(f"\nTotal Active Rows in Excel Sheet1: {len(excel_rows)}")
if excel_rows:
    print("First 3 Excel Rows:")
    for row in excel_rows[:3]:
        print(" ", row)
    print("Last 3 Excel Rows:")
    for row in excel_rows[-3:]:
        print(" ", row)

# 2. Audit PDF
with pdfplumber.open(pdf_path) as pdf:
    print(f"\nTotal Pages in 0.pdf: {len(pdf.pages)}")
    for p_idx, page in enumerate(pdf.pages):
        text = page.extract_text() or ""
        first_line = text.splitlines()[0] if text.splitlines() else ""
        print(f"  Page {p_idx+1}: {len(text)} chars | First line: {first_line[:60]}")

# 3. Check Header on Page 1
with pdfplumber.open(pdf_path) as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    # Find Periode, Nama, Cabang, etc.
    p1_text = p1.extract_text()
    print("\nPage 1 Full Text:")
    print(p1_text[:1000])

