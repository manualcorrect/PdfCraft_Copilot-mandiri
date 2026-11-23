import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        # header right top words: 500 <= x0 <= 580, top < 140
        hw = [w for w in words if 520 <= w['x0'] <= 580 and w['top'] < 140]
        hw.sort(key=lambda w: (round(w['top'], 1), w['x0']))
        print(f"Page {p_idx+1} header right:")
        for w in hw:
            print(f"  {w['text']} top={w['top']} x0={w['x0']}")
