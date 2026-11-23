import os
import openpyxl
import pdfplumber

target_dir = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug"
pdf_path = os.path.join(target_dir, "0.pdf")
excel_path = os.path.join(target_dir, "Template_Mutasi_AUG.xlsx")

print("=== 1. AUDIT EXCEL FILE ===")
wb = openpyxl.load_workbook(excel_path, data_only=True)
print("Sheet names:", wb.sheetnames)

for sname in wb.sheetnames:
    ws = wb[sname]
    print(f"\n--- Sheet: {sname} (max_row={ws.max_row}, max_column={ws.max_column}) ---")
    # print first 15 rows
    for r in range(1, min(20, ws.max_row + 1)):
        row_vals = [ws.cell(r, c).value for c in range(1, min(12, ws.max_column + 1))]
        if any(v is not None for v in row_vals):
            print(f"Row {r:2d}: {row_vals}")

print("\n=== 2. AUDIT PDF FILE ===")
with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    p0 = pdf.pages[0]
    words = p0.extract_words()
    print("\nHeader words in Page 1 (top < 300):")
    for w in words:
        if w['top'] < 300:
            print(f"  {w['text']:<25} top={w['top']:.2f} x0={w['x0']:.2f}")
            
    # Extract total transactions in 0.pdf
    wib_count = 0
    for idx, page in enumerate(pdf.pages):
        p_words = page.extract_words()
        page_wibs = [w for w in p_words if w['text'] == 'WIB']
        wib_count += len(page_wibs)
        print(f"Page {idx+1}: {len(page_wibs)} transactions")
    print(f"Total transactions in 0.pdf: {wib_count}")
