import pdfplumber

aug_pdf = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\REK_KEISYA_AUG_OUTPUT_1.pdf"
with pdfplumber.open(aug_pdf) as pdf:
    p1 = pdf.pages[0]
    for c in p1.chars:
        if c['top'] < 130 and c['x0'] > 500:
            print(f"Char: '{c['text']}', font: {c.get('fontname')}, size: {c.get('size')}, matrix: {c.get('matrix')}")
