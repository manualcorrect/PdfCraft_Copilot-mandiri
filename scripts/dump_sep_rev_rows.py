import pdfplumber
import json

sep_rev = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_sep byk harus revisi.pdf"

rows = []
with pdfplumber.open(sep_rev) as pdf:
    for page_idx, page in enumerate(pdf.pages, 1):
        words = page.extract_words()
        no_words = [w for w in words if abs(w['x0'] - 20.0) < 5 and 200 < w['top'] < 780 and w['text'].isdigit()]
        no_words.sort(key=lambda w: w['top'])
        for nw in no_words:
            no_val = int(nw['text'])
            y = nw['top']
            row_words = [w for w in words if abs(w['top'] - y) < 16]
            
            # Date & time
            d_words = [w for w in row_words if 45 <= w['x0'] < 118 and abs(w['top'] - (y - 4)) < 8]
            t_words = [w for w in row_words if 45 <= w['x0'] < 118 and abs(w['top'] - (y + 5)) < 8]
            d_str = " ".join(w['text'] for w in sorted(d_words, key=lambda x: x['x0']))
            t_str = " ".join(w['text'] for w in sorted(t_words, key=lambda x: x['x0']))
            
            # Nominal & Saldo
            nom_words = [w for w in row_words if 360 <= w['x0'] < 460]
            sal_words = [w for w in row_words if 460 <= w['x0'] < 580]
            nom_str = " ".join(w['text'] for w in sorted(nom_words, key=lambda x: x['x0']))
            sal_str = " ".join(w['text'] for w in sorted(sal_words, key=lambda x: x['x0']))
            
            # Keterangan
            ket_words = [w for w in row_words if 118 <= w['x0'] < 360]
            lines_dict = {}
            for kw in ket_words:
                line_k = round(kw['top'] / 3.0) * 3
                lines_dict.setdefault(line_k, []).append(kw)
            ket_lines = []
            for lk in sorted(lines_dict.keys()):
                l_words = sorted(lines_dict[lk], key=lambda w: w['x0'])
                ket_lines.append(" ".join(w['text'] for w in l_words))
                
            rows.append({
                "page": page_idx,
                "no": no_val,
                "row_y": y,
                "date": d_str,
                "time": t_str,
                "nom": nom_str,
                "sal": sal_str,
                "ket": ket_lines
            })

with open("scratch/sep_rev_rows.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2, ensure_ascii=False)

print(f"Dumped {len(rows)} rows to scratch/sep_rev_rows.json")
for r in rows:
    print(f"Row {r['no']:2d} (P{r['page']}): {r['date']} | {r['time']} | {r['nom']} | {r['sal']}")
    for l in r['ket']:
        print(f"      {l}")
