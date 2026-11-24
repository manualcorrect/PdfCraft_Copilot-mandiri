import pdfplumber, openpyxl, os

ref_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\REK GAJI SEPTEMBER IBNU AGUN.pdf'
with pdfplumber.open(ref_path) as pdf:
    print("Total pages in Ibnu Agun Sep:", len(pdf.pages))
    p1 = pdf.pages[0]
    words = p1.extract_words()
    print("\n=== Header Page 1 Ibnu Agun Sep ===")
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        if w['top'] < 160:
            print(f"{w['top']:.2f}, {w['x0']:.2f}: {w['text']}")

    # Find salary transaction
    print("\n=== Salary Transaction Search in Ibnu Agun Sep ===")
    for p_idx, page in enumerate(pdf.pages):
        text = page.extract_text()
        if "BENDI" in text or "6.000.000" in text or "5.500.000" in text:
            print(f"Salary found on Page {p_idx+1}")
            words = page.extract_words()
            for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
                if "BENDI" in w['text'] or "5411078192" in w['text'] or "CENAIDJA" in w['text']:
                    print(f"Top {w['top']:.2f}, x0={w['x0']:.2f}-{w['x1']:.2f}: {w['text']}")

    # Find closing fee
    last_page = pdf.pages[-1]
    print(f"\n=== Last Page (Page {len(pdf.pages)}) Ibnu Agun Sep ===")
    words = last_page.extract_words()
    for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
        if 350 <= w['top'] <= 460:
            print(f"Top {w['top']:.2f}, x0={w['x0']:.2f}-{w['x1']:.2f}: {w['text']}")
