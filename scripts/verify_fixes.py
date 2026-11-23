import pdfplumber

pdf_path = r"output\REK_GALANG_AUG_2026_STANDARDIZED.pdf"

with pdfplumber.open(pdf_path) as pdf:
    # 1. Check Page 2 Row 22 (the +6.700.000 transaction)
    p2 = pdf.pages[1]
    words2 = p2.extract_words()
    table_words2 = [w for w in words2 if 200 <= w['top'] <= 800]
    r22_w = [w for w in table_words2 if 15 <= w['x0'] <= 35 and w['text'] == '22'][0]
    r22_top = r22_w['top']
    d22_w = [w['text'] for w in table_words2 if abs(w['top'] - (r22_top - 4)) < 4 and 45 <= w['x0'] <= 110]
    t22_w = [w['text'] for w in table_words2 if abs(w['top'] - (r22_top + 5)) < 4 and 45 <= w['x0'] <= 110]
    n22_w = [w['text'] for w in table_words2 if abs(w['top'] - r22_top) < 6 and 365 <= w['x0'] <= 455]
    print(f"Row 22 check:")
    print(f"  Date: {' '.join(d22_w)}")
    print(f"  Time: {' '.join(t22_w)}")
    print(f"  Nominal: {' '.join(n22_w)}")
    
    # 2. Check Page 1 Row 1 Description positions
    p1 = pdf.pages[0]
    words1 = p1.extract_words()
    desc1_words = [w for w in words1 if 330 <= w['top'] <= 365 and 120 <= w['x0'] <= 250]
    lines = {}
    for w in desc1_words:
        lines.setdefault(round(w['top'], 1), []).append(w['text'])
    print(f"\nRow 1 Description lines:")
    for top in sorted(lines.keys()):
        print(f"  top={top:5.1f}: {' '.join(lines[top])}")
