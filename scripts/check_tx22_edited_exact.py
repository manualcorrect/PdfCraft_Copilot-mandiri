import pdfplumber

aug_edited = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_edited ketengangan.pdf"
with pdfplumber.open(aug_edited) as pdf:
    p2 = pdf.pages[1]
    words = [w for w in p2.extract_words() if abs(w['top'] - 733.92) < 25 and 120 <= w['x0'] <= 365]
    lines = {}
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        lines.setdefault(round(w['top'], 1), []).append(w['text'])
    print("--- Row 22 in EDITED PDF ---")
    for top, ws in sorted(lines.items()):
        print(f"  top={top:5.1f}: {' '.join(ws)}")
