import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf"
with pdfplumber.open(pdf_path) as pdf:
    tx_count = 0
    for p_num in range(1, 4):
        page = pdf.pages[p_num - 1]
        words = page.extract_words()
        base_y = 343.92 if p_num == 1 else 227.92
        wibs = sorted([w for w in words if w["text"] == "WIB" and w["top"] > 200], key=lambda x: x["top"])
        print(f"\n=== PAGE {p_num} ({len(wibs)} WIB anchors) ===")
        for r_i, w in enumerate(wibs):
            tx_count += 1
            row_y = base_y + r_i * 46.00
            
            # Date words
            date_words = [d["text"] for d in words if 0 < (w["top"] - d["top"]) < 15 and 45 <= d["x0"] <= 95]
            time_words = [t["text"] for t in words if abs(t["top"] - w["top"]) < 3 and t["x1"] <= w["x0"] + 1]
            date_str = " ".join(date_words)
            time_str = " ".join(time_words) + " WIB"
            
            # Keterangan
            row_words = [cw for cw in words if 115 <= cw["x0"] <= 365 and abs(cw["top"] - row_y) < 22]
            lines = {}
            for cw in sorted(row_words, key=lambda x: (x["top"], x["x0"])):
                lines.setdefault(round(cw["top"], 1), []).append(cw["text"])
            ket_lines = [" ".join(lines[top]) for top in sorted(lines.keys())]
            ket_str = "\n".join(ket_lines)
            
            # Nominal
            nom_words = [n["text"] for n in words if 370 <= n["x0"] <= 450 and abs(n["top"] - (w["top"] - 3)) < 15]
            nom_str = " ".join(nom_words)
            
            # Saldo
            sal_words = [s["text"] for s in words if 480 <= s["x0"] <= 585 and abs(s["top"] - (w["top"] - 3)) < 15]
            sal_str = " ".join(sal_words)
            
            print(f"Tx {tx_count:2d} (P{p_num} R{r_i}): {date_str} {time_str} | Nom: {nom_str:>13} | Sal: {sal_str:>13}")
            print(f"    Ket: {repr(ket_str)}")
