import openpyxl
import pdfplumber
import re

pdf_path = "output/test_fix_edited_pdf.pdf"
excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\Template_Mutasi_Aug.xlsx"

# 1. Extract the 37 transactions from the perfected PDF
txs = []
with pdfplumber.open(pdf_path) as pdf:
    for p_num, page in enumerate(pdf.pages, 1):
        words = page.extract_words()
        base_y = 343.92 if p_num == 1 else 227.92
        wibs = sorted([w for w in words if w['text'] == 'WIB' and w['top'] > 200], key=lambda x: x['top'])
        for r_i, w in enumerate(wibs):
            row_y = base_y + r_i * 46.00
            
            # Date
            date_words = [d['text'] for d in words if 0 < (w['top'] - d['top']) < 15 and 45 <= d['x0'] <= 95]
            time_words = [t['text'] for t in words if abs(t['top'] - w['top']) < 3 and t['x1'] <= w['x0'] + 1]
            date_str = " ".join(date_words)
            time_str = " ".join(time_words) + " WIB"
            
            # Keterangan
            row_words = [cw for cw in words if 115 <= cw['x0'] <= 365 and abs(cw['top'] - row_y) < 22]
            lines = {}
            for cw in sorted(row_words, key=lambda x: (x['top'], x['x0'])):
                lines.setdefault(round(cw['top'], 1), []).append(cw['text'])
            ket_lines = [" ".join(lines[top]) for top in sorted(lines.keys())]
            ket_str = "\n".join(ket_lines)
            
            # Nominal
            nom_words = [n['text'] for n in words if 370 <= n['x0'] <= 450 and abs(n['top'] - (w['top'] - 3)) < 15]
            nom_str = " ".join(nom_words)
            
            # Saldo
            sal_words = [s['text'] for s in words if 480 <= s['x0'] <= 585 and abs(s['top'] - (w['top'] - 3)) < 15]
            sal_str = " ".join(sal_words)
            
            txs.append({
                "no": len(txs) + 1,
                "date": date_str,
                "time": time_str,
                "ket": ket_str,
                "nom_str": nom_str,
                "sal_str": sal_str
            })

print(f"Extracted {len(txs)} transactions from PDF.")

# 2. Update Excel
wb = openpyxl.load_workbook(excel_path)
ws2 = wb["Tabel_Mutasi"]

# Map transactions to active rows
tx_cursor = 0
for r in range(6, ws2.max_row + 1):
    nom_cell = ws2.cell(r, 5).value
    if nom_cell is None or str(nom_cell).strip() == '':
        continue
    
    # check if zero row
    nom_raw = str(nom_cell).replace(".", "").replace(",", ".").replace("+", "").strip()
    try:
        if abs(float(nom_raw)) < 0.001:
            continue
    except:
        pass
        
    t = txs[tx_cursor]
    tx_cursor += 1
    
    ws2.cell(r, 1).value = t["no"]
    ws2.cell(r, 2).value = t["date"]
    ws2.cell(r, 3).value = t["time"]
    ws2.cell(r, 4).value = t["ket"]
    
print(f"Updated {tx_cursor} transaction rows in Excel Tabel_Mutasi.")
out_excel = "output/Template_Mutasi_Aug_Synchronized.xlsx"
wb.save(out_excel)
print(f"Saved {out_excel} successfully!")
try:
    import shutil
    shutil.copyfile(out_excel, excel_path)
    print(f"Successfully updated {excel_path} directly!")
except Exception as e:
    print(f"Note: {excel_path} is currently locked by Excel: {e}")

