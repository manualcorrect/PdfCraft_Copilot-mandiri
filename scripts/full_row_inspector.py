import pdfplumber

def get_full_row_data(pdf_path):
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for p_idx, p in enumerate(pdf.pages):
            words = p.extract_words()
            no_words = [w for w in words if abs(w['x0'] - 20.0) < 5 and 200 < w['top'] < 780 and w['text'].isdigit()]
            no_words.sort(key=lambda w: w['top'])
            for nw in no_words:
                no_val = int(nw['text'])
                y = nw['top']
                row_words = [w for w in words if abs(w['top'] - y) < 16]
                
                dt_words = [w for w in row_words if 45 <= w['x0'] < 118]
                ket_words = [w for w in row_words if 118 <= w['x0'] < 360]
                nom_words = [w for w in row_words if 360 <= w['x0'] < 460]
                sal_words = [w for w in row_words if 460 <= w['x0'] < 580]
                
                dt_words.sort(key=lambda w: (round(w['top'], 1), w['x0']))
                nom_words.sort(key=lambda w: w['x0'])
                sal_words.sort(key=lambda w: w['x0'])
                
                # group ket lines
                lines_dict = {}
                for kw in ket_words:
                    line_k = round(kw['top'] / 3.0) * 3
                    lines_dict.setdefault(line_k, []).append(kw)
                ket_lines = []
                for lk in sorted(lines_dict.keys()):
                    l_words = sorted(lines_dict[lk], key=lambda w: w['x0'])
                    ket_lines.append(" ".join(w['text'] for w in l_words))
                
                rows.append({
                    "page": p_idx + 1,
                    "no": no_val,
                    "y": y,
                    "dt": " ".join(w['text'] for w in dt_words),
                    "ket": ket_lines,
                    "nom": " ".join(w['text'] for w in nom_words),
                    "sal": " ".join(w['text'] for w in sal_words),
                })
    return rows

rev_data = get_full_row_data(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_sep byk harus revisi.pdf")
orig_data = get_full_row_data(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026.pdf")
ref_data = get_full_row_data(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf")

print(f"Total rows: rev={len(rev_data)}, orig={len(orig_data)}, ref={len(ref_data)}")

for i in range(len(rev_data)):
    r_rev = rev_data[i]
    r_orig = orig_data[i] if i < len(orig_data) else None
    r_ref = ref_data[i] if i < len(ref_data) else None
    
    print(f"\nRow {r_rev['no']} (P{r_rev['page']}):")
    print(f"  DT : rev='{r_rev['dt']}' | orig='{r_orig['dt'] if r_orig else ''}'")
    print(f"  KET: rev={r_rev['ket']}")
    print(f"       orig={r_orig['ket'] if r_orig else ''}")
    print(f"  NOM: rev='{r_rev['nom']}' | orig='{r_orig['nom'] if r_orig else ''}'")
    print(f"  SAL: rev='{r_rev['sal']}' | orig='{r_orig['sal'] if r_orig else ''}'")
