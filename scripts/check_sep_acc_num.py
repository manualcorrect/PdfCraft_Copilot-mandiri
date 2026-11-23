import pdfplumber

with pdfplumber.open(r"output\REK_GALANG_SEP_2026_CHRONOLOGICAL.pdf") as pdf:
    for c in pdf.pages[0].chars:
        if 140 <= c['x0'] <= 230 and abs(c['top'] - 190) < 5:
            print(f"SEP char: {repr(c['text'])} x0={c['x0']:.1f}")
