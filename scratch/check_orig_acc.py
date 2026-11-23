import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf") as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    acc_words = [w for w in words if 180 <= w['top'] <= 210 and w['x0'] < 250]
    print("ORIGINAL 0.pdf words around y=180-210 on Page 1:")
    for w in acc_words:
        print(f"'{w['text']}' at x0={w['x0']:.1f}, x1={w['x1']:.1f}, top={w['top']:.1f}")
