import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
import pdfplumber

pdf_path = "output/REK_GALANG_JUL_2026_STANDARDIZED.pdf"

with pdfplumber.open(pdf_path) as pdf:
    p2 = pdf.pages[1]
    words = p2.extract_words()
    
    # Tx 18 is row 8 on page 2: Y_base = 227.92 + 7 * 46 = 549.92
    row8_words = [w for w in words if abs(w['top'] - 549.92) < 25.0 and 120 <= w['x0'] <= 350]
    
    # Group by line
    lines = {}
    for w in row8_words:
        matched = False
        for y_k in lines:
            if abs(w['top'] - y_k) < 3.0:
                lines[y_k].append(w)
                matched = True
                break
        if not matched:
            lines[w['top']] = [w]
            
    print(f"=== PAGE 2 ROW 8 (TX 18) LINES COUNT: {len(lines)} ===")
    for y_k in sorted(lines.keys()):
        l_str = " ".join([w['text'] for w in sorted(lines[y_k], key=lambda x: x['x0'])])
        x0 = min(w['x0'] for w in lines[y_k])
        x1 = max(w['x1'] for w in lines[y_k])
        print(f"  Y={y_k:.2f} (X={x0:.2f}-{x1:.2f}): {l_str}")
