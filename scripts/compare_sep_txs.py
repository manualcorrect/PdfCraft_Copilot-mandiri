import pdfplumber, openpyxl

wb = openpyxl.load_workbook(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\Template_Mutasi_SEP.xlsx')
ws = wb['Tabel_Mutasi']

excel_txs = []
for r in range(6, ws.max_row + 1):
    nom = ws.cell(r, 5).value
    saldo = ws.cell(r, 7).value
    desc = ws.cell(r, 4).value
    if nom is not None and abs(float(nom)) > 0.001:
        excel_txs.append({
            'row': r,
            'nom': float(nom),
            'saldo': float(saldo),
            'desc': desc
        })

print(f"Excel active tx count: {len(excel_txs)}")

# Inspect 0.pdf descriptions and nominals
pdf_txs = []
with pdfplumber.open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\0.pdf') as pdf:
    for p_num in range(1, 5):
        page = pdf.pages[p_num - 1]
        words = page.extract_words()
        base_y = 343.92 if p_num == 1 else 227.92
        wibs = sorted([w for w in words if w["text"] == "WIB" and w["top"] > 200], key=lambda x: x["top"])
        for r_i, w in enumerate(wibs):
            row_y = base_y + r_i * 46.00
            
            # Keterangan words
            row_words = [cw for cw in words if 115 <= cw["x0"] <= 365 and abs(cw["top"] - row_y) < 22]
            lines = {}
            for cw in sorted(row_words, key=lambda x: (x["top"], x["x0"])):
                lines.setdefault(round(cw["top"], 1), []).append(cw["text"])
            ket_lines = [" ".join(lines[top]) for top in sorted(lines.keys())]
            ket_str = "\n".join(ket_lines)
            
            # Nominal
            nom_words = [cw for cw in words if 350 <= cw["x0"] <= 450 and abs(cw["top"] - row_y) < 15]
            nom_str = " ".join([cw["text"] for cw in nom_words])
            
            # Saldo
            sal_words = [cw for cw in words if cw["x0"] > 500 and abs(cw["top"] - row_y) < 15]
            sal_str = " ".join([cw["text"] for cw in sal_words])
            
            pdf_txs.append({
                'page': p_num,
                'row_idx': r_i,
                'top': row_y,
                'desc': ket_str,
                'nom_str': nom_str,
                'sal_str': sal_str
            })

print(f"0.pdf active tx count: {len(pdf_txs)}")

print("\n--- DETAILED COMPARISON TABLE ---")
diff_noms = []
for i in range(46):
    ex = excel_txs[i]
    pf = pdf_txs[i]
    nom_match = (f"{abs(ex['nom']):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") in pf['nom_str'])
    status = "SAME_NOM" if nom_match else "DIFF_NOM"
    if not nom_match:
        diff_noms.append(i + 1)
    print(f"Tx {i+1:2d} (P{pf['page']} R{pf['row_idx']+1:2d}): Excel={ex['nom']:>11,.2f} | PDF={pf['nom_str']:<14} | {status} | Desc: {repr(pf['desc'][:40])}")

print(f"\nTransactions with different nominals: {diff_noms}")
