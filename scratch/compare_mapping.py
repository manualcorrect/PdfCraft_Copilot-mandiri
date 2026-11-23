import openpyxl
import pdfplumber

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\Template_Mutasi_Aug.xlsx"
pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"

print("========================================")
print("COMPARING 37 ROWS IN EXCEL VS 37 ROWS IN 2.pdf")
print("========================================")

wb = openpyxl.load_workbook(excel_path, data_only=True)
ws2 = wb["Tabel_Mutasi"]

excel_tx = []
for r in range(6, ws2.max_row + 1):
    nom = ws2.cell(r, 5).value
    sal = ws2.cell(r, 7).value
    tgl = ws2.cell(r, 2).value
    jam = ws2.cell(r, 3).value
    uraian = ws2.cell(r, 4).value
    if nom is not None and nom != 0:
        excel_tx.append({
            "excel_row": r,
            "nominal": nom,
            "saldo": sal,
            "tanggal": tgl,
            "jam": jam,
            "uraian": uraian
        })

print(f"Total valid transactions in Excel: {len(excel_tx)}")

with pdfplumber.open(pdf_path) as pdf:
    pdf_rows = []
    for page_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 320 if page_idx == 0 else 200
        table_words = [w for w in words if min_top <= w["top"] <= 800]
        nos = sorted([w for w in table_words if 15 <= w["x0"] <= 35 and w["text"].isdigit()], key=lambda x: x["top"])
        for n in nos:
            row_words = [w for w in table_words if abs(w["top"] - n["top"]) < 20]
            desc_words = [w for w in row_words if 115 <= w["x0"] <= 360]
            nom_words = [w for w in row_words if 360 <= w["x0"] <= 450]
            saldo_words = [w for w in row_words if 490 <= w["x0"] <= 585]
            
            pdf_rows.append({
                "page": page_idx + 1,
                "orig_no": n["text"],
                "desc": " ".join(w["text"] for w in desc_words),
                "orig_nom": " ".join(w["text"] for w in nom_words),
                "orig_saldo": " ".join(w["text"] for w in saldo_words)
            })

print(f"Total rows in 2.pdf: {len(pdf_rows)}")

print("\n--- SIDE-BY-SIDE MAPPING ---")
print(f"{'Idx':3s} | {'Pg':2s} | {'PDF No':6s} | {'PDF Orig Desc':35s} | {'PDF Orig Nom':12s} | {'Excel New Nom':14s} | {'Excel New Saldo':16s}")
print("-" * 105)
for i in range(min(len(excel_tx), len(pdf_rows))):
    ex = excel_tx[i]
    pf = pdf_rows[i]
    desc_short = (pf['desc'][:32] + '...') if len(pf['desc']) > 32 else pf['desc']
    print(f"{i+1:3d} | P{pf['page']} | No {pf['orig_no']:3s} | {desc_short:35s} | {pf['orig_nom']:12s} | {ex['nominal']:>12,.2f} | {ex['saldo']:>14,.2f}")
