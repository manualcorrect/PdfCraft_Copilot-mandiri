import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf"
with pdfplumber.open(pdf_path) as pdf:
    p4 = pdf.pages[3]
    for w in sorted(p4.extract_words(), key=lambda x: (x["top"], x["x0"])):
        print(f"P4: {w['text']} at x={w['x0']:.1f}, top={w['top']:.1f}")
