import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\REK GAJI AGUSTUS IBNU AGUN.pdf"
with pdfplumber.open(pdf_path) as pdf:
    p6 = pdf.pages[5]
    print("=== P6 Tx 60 Words ===")
    for w in sorted(p6.extract_words(), key=lambda x: (x["top"], x["x0"])):
        if 360 <= w["top"] <= 450:
            print(f"Top {w['top']:6.2f}, X0 {w['x0']:6.2f}, X1 {w['x1']:6.2f}: {w['text']}")
            
    p7 = pdf.pages[6]
    print("\n=== P7 Tx 75 Words ===")
    for w in sorted(p7.extract_words(), key=lambda x: (x["top"], x["x0"])):
        if 300 <= w["top"] <= 450:
            print(f"Top {w['top']:6.2f}, X0 {w['x0']:6.2f}, X1 {w['x1']:6.2f}: {w['text']}")
