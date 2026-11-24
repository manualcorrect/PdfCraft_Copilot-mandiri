import pdfplumber

pdf_path = "output/REK_WAFIQ_AUG_OUTPUT_1.pdf"
with pdfplumber.open(pdf_path) as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    h_words = [w for w in words if w["top"] < 250]
    for w in sorted(h_words, key=lambda x: (x["top"], x["x0"])):
        print(f"Top: {w['top']:5.1f}, X0: {w['x0']:5.1f}, Text: {w['text']}")
