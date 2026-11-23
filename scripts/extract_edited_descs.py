import pdfplumber

aug_edited = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_edited ketengangan.pdf"

with pdfplumber.open(aug_edited) as pdf:
    global_row = 0
    for p_idx, page in enumerate(pdf.pages, 1):
        words = page.extract_words()
        wibs = sorted([w for w in words if w["text"] == "WIB" and w["top"] > 200], key=lambda x: x["top"])
        print(f"\n================ PAGE {p_idx} ({len(wibs)} rows) ================")
        
        for r_i, w in enumerate(wibs):
            global_row += 1
            # date
            date_words = [d["text"] for d in words if 0 < (w["top"] - d["top"]) < 15 and 45 <= d["x0"] <= 95]
            time_words = [t["text"] for t in words if abs(t["top"] - w["top"]) < 3 and t["x1"] <= w["x0"] + 1]
            date_str = " ".join(date_words)
            time_str = " ".join(time_words) + " WIB"
            
            # nominal
            nom_words = [n["text"] for n in words if 370 <= n["x0"] <= 450 and abs(n["top"] - (w["top"] - 3)) < 15]
            nom_str = " ".join(nom_words)
            
            # saldo
            sal_words = [s["text"] for s in words if 480 <= s["x0"] <= 585 and abs(s["top"] - (w["top"] - 3)) < 15]
            sal_str = " ".join(sal_words)
            
            # Now let's inspect ALL words in the keterangan area for this row
            # Determine vertical boundary for this row:
            # from w['top'] - 12 down to next row's w['top'] - 12 (or w['top'] + 33 if last row)
            top_min = w["top"] - 12
            if r_i + 1 < len(wibs):
                top_max = wibs[r_i + 1]["top"] - 12
            else:
                top_max = w["top"] + 35
                
            row_words = [cw for cw in words if 95 <= cw["x0"] <= 375 and top_min <= cw["top"] < top_max]
            # sort into lines by top coordinate
            lines = {}
            for cw in sorted(row_words, key=lambda x: (x["top"], x["x0"])):
                line_key = round(cw["top"] / 5.0) * 5
                lines.setdefault(line_key, []).append(cw)
                
            line_strs = []
            for lk in sorted(lines.keys()):
                l_words = sorted(lines[lk], key=lambda x: x["x0"])
                line_strs.append(" ".join([x["text"] for x in l_words]))
                
            print(f"Row {global_row:2d} (P{p_idx}:{r_i+1:2d}) | {date_str} {time_str} | Nom: {nom_str} | Sal: {sal_str}")
            print(f"   Lines ({len(line_strs)}):")
            for ls in line_strs:
                print(f"     -> {ls}")
