import pdfplumber

ref_2 = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"
with pdfplumber.open(ref_2) as pdf:
    # Look at row 22 in 2.pdf
    p2 = pdf.pages[1]
    words = [w for w in p2.extract_words() if abs(w['top'] - 733.92) < 22 and 120 <= w['x0'] <= 365]
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        print(f"{w['text']:<25} top={w['top']:.2f}, x0={w['x0']:.2f}, x1={w['x1']:.2f}")

print("\n--- Row 22 in 3.pdf (SEP) ---")
ref_3 = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"
with pdfplumber.open(ref_3) as pdf:
    p2 = pdf.pages[1]
    words = [w for w in p2.extract_words() if abs(w['top'] - 733.92) < 22 and 120 <= w['x0'] <= 365]
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        print(f"{w['text']:<25} top={w['top']:.2f}, x0={w['x0']:.2f}, x1={w['x1']:.2f}")
