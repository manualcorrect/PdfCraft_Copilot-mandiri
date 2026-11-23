import openpyxl
import pdfplumber

excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\Template_Mutasi_SEP.xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb["Tabel_Mutasi"]
excel_txs = []
for r in range(6, ws.max_row + 1):
    nom = ws.cell(r, 5).value
    sal = ws.cell(r, 7).value
    if nom is not None and str(nom).strip() != "":
        try:
            val = float(nom)
            if abs(val) > 0.001:
                excel_txs.append({"r": r, "nom": val, "sal": float(sal)})
        except:
            pass

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"
pdf_txs = []
with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        wibs = sorted([w for w in words if w["text"] == "WIB"], key=lambda x: x["top"])
        for w in wibs:
            nom_words = [x for x in words if abs(x["top"] - w["top"]) < 15 and 370 <= x["x0"] <= 460]
            nom_str = "".join([x["text"] for x in nom_words])
            nom_val = float(nom_str.replace("+", "").replace(".", "").replace(",", "."))
            pdf_txs.append({"nom": nom_val, "nom_str": nom_str})

print(f"Excel rows: {len(excel_txs)}, PDF rows: {len(pdf_txs)}")

for i in range(max(len(excel_txs), len(pdf_txs))):
    e = excel_txs[i] if i < len(excel_txs) else None
    p = pdf_txs[i] if i < len(pdf_txs) else None
    e_val = f"{e['nom']:>14,.2f}" if e else " " * 14
    p_val = f"{p['nom']:>14,.2f}" if p else " " * 14
    match = "==" if (e and p and abs(e["nom"] - p["nom"]) < 0.01) else "!="
    print(f"Row {i+1:2d}: Excel={e_val} {match} PDF={p_val}")
