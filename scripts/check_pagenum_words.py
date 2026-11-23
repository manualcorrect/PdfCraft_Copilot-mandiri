import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf") as pdf:
    for p_idx in range(len(pdf.pages)):
        p = pdf.pages[p_idx]
        words = [w for w in p.extract_words() if 90 <= w['top'] <= 125 and w['x0'] > 520]
        for w in words:
            if 'dari' in w['text'] or 'of' in w['text'] or w['text'] == '13':
                print(f"Page {p_idx+1}: word='{w['text']}' x0={w['x0']:.2f} x1={w['x1']:.2f} top={w['top']:.2f}")
