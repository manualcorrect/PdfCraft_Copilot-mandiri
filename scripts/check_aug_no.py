import pdfplumber

aug_pdf = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\REK_KEISYA_AUG_OUTPUT_1.pdf"
with pdfplumber.open(aug_pdf) as pdf:
    for p_idx in range(len(pdf.pages)):
        p = pdf.pages[p_idx]
        words = p.extract_words()
        no_words = [w for w in words if 15 <= w['x0'] <= 35 and 200 <= w['top'] <= 780]
        no_words.sort(key=lambda w: w['top'])
        print(f"Page {p_idx+1} No column: {[w['text'] for w in no_words]}")
