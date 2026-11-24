import pdfplumber
import openpyxl

pdf_orig = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf"
pdf_final = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\REK_WAFIQ_AUG_OUTPUT_1.pdf"
excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\Template_Mutasi_AUG.xlsx"

def extract_descs(path):
    txs = []
    with pdfplumber.open(path) as pdf:
        for p_num in range(1, 4):
            page = pdf.pages[p_num - 1]
            words = page.extract_words()
            base_y = 343.92 if p_num == 1 else 227.92
            wibs = sorted([w for w in words if w["text"] == "WIB" and w["top"] > 200], key=lambda x: x["top"])
            for r_i, w in enumerate(wibs):
                row_y = base_y + r_i * 46.00
                row_words = [cw for cw in words if 115 <= cw["x0"] <= 365 and abs(cw["top"] - row_y) < 22]
                lines = {}
                for cw in sorted(row_words, key=lambda x: (x["top"], x["x0"])):
                    lines.setdefault(round(cw["top"], 1), []).append(cw["text"])
                ket_lines = [" ".join(lines[top]) for top in sorted(lines.keys())]
                ket_str = "\n".join(ket_lines)
                
                nom_words = [n["text"] for n in words if 370 <= n["x0"] <= 450 and abs(n["top"] - (w["top"] - 3)) < 15]
                nom_str = " ".join(nom_words)
                
                sal_words = [s["text"] for s in words if 480 <= s["x0"] <= 585 and abs(s["top"] - (w["top"] - 3)) < 15]
                sal_str = " ".join(sal_words)
                
                date_words = [d["text"] for d in words if 0 < (w["top"] - d["top"]) < 15 and 45 <= d["x0"] <= 95]
                time_words = [t["text"] for t in words if abs(t["top"] - w["top"]) < 3 and t["x1"] <= w["x0"] + 1]
                
                txs.append({
                    "no": len(txs) + 1,
                    "date": " ".join(date_words),
                    "time": " ".join(time_words) + " WIB",
                    "desc": ket_str,
                    "nom": nom_str,
                    "sal": sal_str
                })
    return txs

tx_orig = extract_descs(pdf_orig)
tx_final = extract_descs(pdf_final)

wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb["Tabel_Mutasi"]

print(f"Total Tx: {len(tx_orig)}")
changes = []
same = []

for i in range(len(tx_orig)):
    o = tx_orig[i]
    f = tx_final[i]
    ex_desc = ws.cell(i + 6, 4).value
    ex_nom = ws.cell(i + 6, 5).value
    
    is_changed = (o["desc"].replace(" ", "").replace("\n", "") != f["desc"].replace(" ", "").replace("\n", ""))
    info = {
        "no": i + 1,
        "orig_desc": o["desc"],
        "final_desc": f["desc"],
        "excel_desc": ex_desc,
        "orig_nom": o["nom"],
        "final_nom": f["nom"],
        "excel_nom": ex_nom,
        "date": f["date"],
        "time": f["time"],
        "is_changed": is_changed
    }
    if is_changed:
        changes.append(info)
    else:
        same.append(info)

print(f"\n--- TOTAL DIUBAH: {len(changes)} BARIS ---")
for c in changes:
    print(f"\n[Tx {c['no']:2d}] Nominal: {c['final_nom']} | Tanggal: {c['date']} {c['time']}")
    print(f"  SEMULA (0.pdf):")
    for l in c['orig_desc'].split('\n'):
        print(f"    {l}")
    print(f"  MENJADI:")
    for l in c['final_desc'].split('\n'):
        print(f"    {l}")

print(f"\n--- TOTAL TIDAK DIUBAH (SAMA DENGAN 0.PDF): {len(same)} BARIS ---")
for s in same:
    one_line = " ".join(s['final_desc'].split('\n'))
    print(f"Tx {s['no']:2d}: {s['final_nom']:>12} | {s['date']} | {one_line[:60]}")
