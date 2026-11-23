import pdfplumber

pdf_path = "output/REK_GALANG_SEP_2026_PERFECT.pdf"

print("==================================================")
print("VERIFYING PERFECT SEP STATEMENT")
print("==================================================")

with pdfplumber.open(pdf_path) as pdf:
    for page_idx, page in enumerate(pdf.pages, 1):
        print(f"\n--- Page {page_idx} ---")
        words = page.extract_words()
        no_words = [w for w in words if abs(w['x0'] - 20.0) < 5 and 200 < w['top'] < 780 and w['text'].isdigit()]
        no_words.sort(key=lambda w: w['top'])
        for nw in no_words:
            no_val = int(nw['text'])
            y = nw['top']
            
            # Words in this row
            row_words = [w for w in words if abs(w['top'] - y) < 18]
            d_words = [w for w in row_words if 45 <= w['x0'] < 118 and abs(w['top'] - (y - 4)) < 8]
            t_words = [w for w in row_words if 45 <= w['x0'] < 118 and abs(w['top'] - (y + 5)) < 8]
            ket_words = [w for w in row_words if 118 <= w['x0'] < 360]
            nom_words = [w for w in row_words if 360 <= w['x0'] < 460]
            sal_words = [w for w in row_words if 460 <= w['x0'] < 580]
            
            d_str = " ".join(w['text'] for w in sorted(d_words, key=lambda x: x['x0']))
            t_str = " ".join(w['text'] for w in sorted(t_words, key=lambda x: x['x0']))
            nom_str = " ".join(w['text'] for w in sorted(nom_words, key=lambda x: x['x0']))
            sal_str = " ".join(w['text'] for w in sorted(sal_words, key=lambda x: x['x0']))
            
            lines_dict = {}
            for kw in ket_words:
                line_k = round(kw['top'] / 3.0) * 3
                lines_dict.setdefault(line_k, []).append(kw)
            ket_lines = []
            for lk in sorted(lines_dict.keys()):
                ket_lines.append(" ".join(w['text'] for w in sorted(lines_dict[lk], key=lambda x: x['x0'])))
                
            ket_x0 = min(w['x0'] for w in ket_words) if ket_words else None
            ket_top = min(w['top'] for w in ket_words) if ket_words else None
            nom_x1 = max(w['x1'] for w in nom_words) if nom_words else None
            sal_x1 = max(w['x1'] for w in sal_words) if sal_words else None
            
            num_lines = len(ket_lines)
            ideal_top = y - (num_lines - 1) * 5.0
            dy = (ket_top - ideal_top) if ket_top is not None else 0.0
            
            nom_x1_str = f"{nom_x1:.1f}" if nom_x1 is not None else "None"
            sal_x1_str = f"{sal_x1:.1f}" if sal_x1 is not None else "None"
            ket_x0_str = f"{ket_x0:.2f}" if ket_x0 is not None else "None"
            ket_top_str = f"{ket_top:.2f}" if ket_top is not None else "None"
            
            print(f"Row {no_val:2d} [y={y:.1f}]: DT='{d_str} {t_str}' | Nom={nom_str} (x1={nom_x1_str}) | Sal={sal_str} (x1={sal_x1_str})")
            print(f"       Ket: x0={ket_x0_str}, top={ket_top_str} (diff={dy:+.2f}pt):")
            for l in ket_lines:
                print(f"         {l}")
