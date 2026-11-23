import pdfplumber

with pdfplumber.open("output/REK_IBNU_SEP_OUTPUT_1.pdf") as pdf:
    p1 = pdf.pages[0]
    chars = [c for c in p1.chars if 115 <= c['top'] <= 135 and 120 <= c['x0'] <= 220]
    for c in chars:
        print(f"Char: '{c['text']}' | ord={ord(c['text'])} | font={c.get('fontname')} | x0={c['x0']:.2f}")
