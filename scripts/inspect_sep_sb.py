import pdfplumber

with pdfplumber.open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\0.pdf') as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    sb_words = [w for w in words if 280 <= w['x0'] <= 580 and 150 <= w['top'] <= 260]
    sb_words.sort(key=lambda w: (round(w['top'], 1), w['x0']))
    rows = {}
    for w in sb_words:
        top_k = round(w['top'], 1)
        rows.setdefault(top_k, []).append(w)
    for top_k, wlist in sorted(rows.items()):
        line_text = " ".join([w['text'] for w in wlist])
        print(f"Top {top_k:5.2f} pt | Content: {line_text}")
