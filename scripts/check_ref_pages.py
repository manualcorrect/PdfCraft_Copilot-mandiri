import pdfplumber

ref_path = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf"

with pdfplumber.open(ref_path) as pdf:
    print(f"Total pages in reference file: {len(pdf.pages)}")
    for idx, page in enumerate(pdf.pages):
        words = [w for w in page.extract_words() if w['top'] < 130 and w['x0'] > 500]
        line = " ".join(w['text'] for w in sorted(words, key=lambda x: (x['top'], x['x0'])))
        print(f"Page {idx+1}: {line}")
        # check last page text
        if idx == len(pdf.pages) - 1:
            print("Last page sample text:")
            print(page.extract_text()[:200])
