import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf") as pdf:
    print("Keisya sep 0.pdf page count:", len(pdf.pages))
    for idx, p in enumerate(pdf.pages):
        words = [w for w in p.extract_words() if w['top'] < 130 and w['x0'] > 500]
        print(f"Page {idx+1}: {' '.join(w['text'] for w in words)}")

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\REK_KEISYA_SEP_OUTPUT_1.pdf") as pdf:
    print("Keisya sep output page count:", len(pdf.pages))
    for idx, p in enumerate(pdf.pages):
        words = [w for w in p.extract_words() if w['top'] < 130 and w['x0'] > 500]
        print(f"Page {idx+1}: {' '.join(w['text'] for w in words)}")
