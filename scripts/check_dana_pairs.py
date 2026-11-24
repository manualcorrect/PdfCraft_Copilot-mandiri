import pdfplumber, openpyxl

wb = openpyxl.load_workbook(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\Template_Mutasi_SEP.xlsx')
ws = wb['Tabel_Mutasi']

excel_txs = []
for r in range(6, ws.max_row + 1):
    nom = ws.cell(r, 5).value
    saldo = ws.cell(r, 7).value
    if nom is not None and abs(float(nom)) > 0.001:
        excel_txs.append((r, float(nom), float(saldo)))

with pdfplumber.open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\0.pdf') as pdf:
    tx_idx = 0
    for p_num in range(1, 5):
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
            ket_str = " | ".join(ket_lines)
            
            ex_r, ex_nom, ex_sal = excel_txs[tx_idx]
            print(f"Tx {tx_idx+1:2d} (Excel R{ex_r:2d}, P{p_num} R{r_i+1:2d}): Nom={ex_nom:>10,.2f} | Ket: {ket_str}")
            tx_idx += 1
