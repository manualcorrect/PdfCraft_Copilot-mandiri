import pdfplumber

ref_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\REK GAJI OKTOBER IBNU AGUN.pdf'
with pdfplumber.open(ref_path) as pdf:
    print("Total pages in Ibnu Agun Okt:", len(pdf.pages))
    p1 = pdf.pages[0]
    words = p1.extract_words()
    print("\n=== Header Page 1 Ibnu Agun Okt ===")
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        if w['top'] < 160:
            print(f"{w['top']:.2f}, {w['x0']:.2f}: {w['text']}")
