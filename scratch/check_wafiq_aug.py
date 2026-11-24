import openpyxl
import pdfplumber
import re

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf"
excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\Template_Mutasi_AUG.xlsx"

wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb["Tabel_Mutasi"]
excel_txs = []
for r in range(6, ws.max_row + 1):
    nom = ws.cell(r, 5).value
    saldo = ws.cell(r, 7).value
    if nom is not None and str(nom) != "-":
        excel_txs.append({
            "row": r,
            "nom": float(nom),
            "saldo": float(saldo),
            "date": ws.cell(r, 2).value,
            "time": ws.cell(r, 3).value,
            "desc": ws.cell(r, 4).value
        })

print(f"Total Excel txs: {len(excel_txs)}")

pdf_txs = []
with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages[:3]):
        text = page.extract_text()
        for line in text.split("\n"):
            m = re.search(r"([+-]\s*[\d\.,]+)\s+([\d\.,]+)$", line.strip())
            if m:
                nom_s = m.group(1).replace(" ", "").replace(".", "").replace(",", ".")
                saldo_s = m.group(2).replace(".", "").replace(",", ".")
                pdf_txs.append({
                    "page": p_idx + 1,
                    "nom": float(nom_s),
                    "saldo": float(saldo_s),
                    "line": line.strip()
                })

print(f"Total PDF txs detected: {len(pdf_txs)}")
diffs = []
for i in range(min(len(excel_txs), len(pdf_txs))):
    e = excel_txs[i]
    p = pdf_txs[i]
    nom_eq = abs(e["nom"] - p["nom"]) < 0.01
    saldo_eq = abs((e["saldo"] + 0.81) - p["saldo"]) < 0.01
    if not nom_eq or not saldo_eq:
        diffs.append((i + 1, e, p))
        print(f"Tx {i+1:2d} (R{e['row']:2d}) DIFF: Excel nom={e['nom']:>12,.2f}, saldo={e['saldo']:>12,.2f} | PDF nom={p['nom']:>12,.2f}, saldo={p['saldo']:>12,.2f}")
    else:
        print(f"Tx {i+1:2d} (R{e['row']:2d}) SAME: nom={e['nom']:>12,.2f}")

print(f"\nTotal differences found: {len(diffs)}")
