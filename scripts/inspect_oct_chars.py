import pdfplumber

with pdfplumber.open("output/REK_GALANG_OCT_2026_CHRONOLOGICAL.pdf") as pdf:
    print("=== Page 1 chars around date row 1 ===")
    for c in pdf.pages[0].chars:
        if 45 <= c["x0"] <= 95 and abs(c["top"] - 340) < 15:
            print(f"Char: {repr(c['text']):8s} font={c['fontname']} adv={c.get('adv')} x0={c['x0']:.1f}")

    print("\n=== Page 1 chars around Cabang ===")
    for c in pdf.pages[0].chars:
        if 45 <= c["x0"] <= 180 and abs(c["top"] - 125) < 15:
            print(f"Char: {repr(c['text']):8s} font={c['fontname']} adv={c.get('adv')} x0={c['x0']:.1f}")

    print("\n=== Page 1 chars around Periode ===")
    for c in pdf.pages[0].chars:
        if 300 <= c["x0"] <= 450 and abs(c["top"] - 100) < 15:
            print(f"Char: {repr(c['text']):8s} font={c['fontname']} adv={c.get('adv')} x0={c['x0']:.1f}")
