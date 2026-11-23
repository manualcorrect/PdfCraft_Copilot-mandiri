import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf") as pdf:
    p1 = pdf.pages[0]
    # words around row 1 (top between 330 and 365)
    words = [w for w in p1.extract_words() if 330 <= w['top'] <= 365]
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        print(f"top={w['top']:.1f}, x0={w['x0']:.1f}, x1={w['x1']:.1f}: {repr(w['text'])}")
