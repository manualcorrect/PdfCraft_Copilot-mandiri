import pdfplumber

pdf_path = "output/REK_WAFIQ_AUG_OUTPUT_1.pdf"
with pdfplumber.open(pdf_path) as pdf:
    p3 = pdf.pages[2]
    words = [w for w in p3.extract_words() if 260 <= w["top"] <= 350 and 115 <= w["x0"] <= 300]
    for w in sorted(words, key=lambda x: (x["top"], x["x0"])):
        print(f"Top: {w['top']:6.2f}, X0: {w['x0']:6.2f}, Text: {w['text']}")
