import pdfplumber

aug_pdf = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\REK_KEISYA_AUG_OUTPUT_1.pdf"
with pdfplumber.open(aug_pdf) as pdf:
    print(f"August PDF total pages: {len(pdf.pages)}")
    for i, p in enumerate(pdf.pages):
        words = [w['text'] for w in p.extract_words() if w['top'] < 130 and w['x0'] > 500]
        print(f"Page {i+1}: {' '.join(words)}")
