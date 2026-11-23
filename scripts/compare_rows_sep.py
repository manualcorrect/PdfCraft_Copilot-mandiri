import pdfplumber
import json

def extract_rows(pdf_path):
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            words = page.extract_words()
            # Find row numbers (No column x0 approx 20.0, top between 210 and 780)
            no_words = [w for w in words if abs(w['x0'] - 20.0) < 5 and w['top'] > 200 and w['top'] < 780 and w['text'].isdigit()]
            no_words.sort(key=lambda w: w['top'])
            
            for nw in no_words:
                no_val = int(nw['text'])
                y = nw['top']
                # find words in this row window [y-8, y+18]
                row_words = [w for w in words if abs(w['top'] - y) < 14]
                
                # classify words by x0:
                # date/time: x0 in [45, 115]
                # ket: x0 in [115, 360]
                # nominal: x0 in [360, 440]
                # saldo: x0 in [480, 580]
                dt_words = [w for w in row_words if 45 <= w['x0'] < 115]
                ket_words = [w for w in row_words if 115 <= w['x0'] < 360]
                nom_words = [w for w in row_words if 360 <= w['x0'] < 460]
                sal_words = [w for w in row_words if 460 <= w['x0'] < 580]
                
                dt_words.sort(key=lambda w: (round(w['top'], 1), w['x0']))
                ket_words.sort(key=lambda w: (round(w['top'], 1), w['x0']))
                nom_words.sort(key=lambda w: w['x0'])
                sal_words.sort(key=lambda w: w['x0'])
                
                # Let's also group ket_words by lines
                lines_dict = {}
                for kw in ket_words:
                    line_k = round(kw['top'] / 5.0) * 5
                    lines_dict.setdefault(line_k, []).append(kw)
                
                ket_lines = []
                for lk in sorted(lines_dict.keys()):
                    l_words = sorted(lines_dict[lk], key=lambda w: w['x0'])
                    ket_lines.append(" ".join(w['text'] for w in l_words))
                
                ket_x0 = ket_words[0]['x0'] if ket_words else None
                ket_top = ket_words[0]['top'] if ket_words else None
                
                rows.append({
                    "page": page_idx + 1,
                    "no": no_val,
                    "y": y,
                    "dt": " ".join(w['text'] for w in dt_words),
                    "ket": "\n".join(ket_lines),
                    "ket_x0": ket_x0,
                    "ket_top": ket_top,
                    "nom": " ".join(w['text'] for w in nom_words),
                    "sal": " ".join(w['text'] for w in sal_words),
                })
    return rows

rev_rows = extract_rows(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_sep byk harus revisi.pdf")
chr_rows = extract_rows(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026_CHRONOLOGICAL.pdf")

print(f"Extracted {len(rev_rows)} rows from rev, {len(chr_rows)} rows from chr")

for r_rev, r_chr in zip(rev_rows, chr_rows):
    diffs = []
    if r_rev['dt'] != r_chr['dt']:
        diffs.append(f"DT: '{r_chr['dt']}' -> '{r_rev['dt']}'")
    if r_rev['ket'] != r_chr['ket']:
        diffs.append(f"KET:\n[chr]:\n{r_chr['ket']}\n[rev]:\n{r_rev['ket']}")
    if r_rev['nom'] != r_chr['nom']:
        diffs.append(f"NOM: '{r_chr['nom']}' -> '{r_rev['nom']}'")
    if r_rev['sal'] != r_chr['sal']:
        diffs.append(f"SAL: '{r_chr['sal']}' -> '{r_rev['sal']}'")
    if r_rev['ket_x0'] is not None and abs(r_rev['ket_x0'] - 124.0) > 1.0:
        diffs.append(f"KET_X0: {r_rev['ket_x0']:.2f}")
        
    print(f"\n--- Row {r_rev['no']} (P{r_rev['page']}) ---")
    if diffs:
        for d in diffs:
            print("  *", d)
    else:
        print("  MATCH")
