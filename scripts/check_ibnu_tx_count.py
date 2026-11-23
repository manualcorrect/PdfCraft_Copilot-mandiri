import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf") as pdf:
    print("Page count in 0.pdf:", len(pdf.pages))
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 310 if p_idx == 0 else 180
        table_words = [w for w in words if min_top <= w['top'] <= 780]
        wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        print(f"Page {p_idx+1}: {len(wibs)} transactions (WIB count)")
