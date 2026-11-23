import pdfplumber

target = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_FINAL.pdf"

with pdfplumber.open(target) as pdf:
    p2 = pdf.pages[1]
    words = p2.extract_words()
    table_words = [w for w in words if 200 <= w['top'] <= 800]
    row_nos = sorted([w for w in table_words if 15 <= w['x0'] <= 35 and w['text'].isdigit()], key=lambda x: x['top'])
    for r_w in row_nos:
        r_top = r_w['top']
        r_no = int(r_w['text'])
        d_words = sorted([w for w in table_words if abs(w['top'] - (r_top - 4)) < 4 and 45 <= w['x0'] <= 110], key=lambda x: x['x0'])
        t_words = sorted([w for w in table_words if abs(w['top'] - (r_top + 5)) < 4 and 45 <= w['x0'] <= 110], key=lambda x: x['x0'])
        n_words = [w for w in table_words if abs(w['top'] - r_top) < 6 and 365 <= w['x0'] <= 455]
        s_words = [w for w in table_words if abs(w['top'] - r_top) < 6 and 490 <= w['x0'] <= 585]
        print(f"Row {r_no:02d} | Date: {' '.join(w['text'] for w in d_words):12} | Time: {' '.join(w['text'] for w in t_words):12} | Nom: {n_words[0]['text'] if n_words else '-':14} | Saldo: {s_words[0]['text'] if s_words else '-'}")
