import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf") as pdf:
    for p_idx, page in enumerate(pdf.pages):
        words = [w for w in page.extract_words() if w['top'] < 130 and w['x0'] > 450]
        line = " ".join(w['text'] for w in sorted(words, key=lambda x: (x['top'], x['x0'])))
        print(f"Page {p_idx+1} header right: {line}")
