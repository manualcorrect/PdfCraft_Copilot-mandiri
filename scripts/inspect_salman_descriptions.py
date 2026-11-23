import sys
import os
sys.path.append(os.path.abspath("src"))
sys.stdout.reconfigure(encoding='utf-8')
import pdfplumber

salman_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Salman\REK APR26.pdf"

with pdfplumber.open(salman_path) as pdf:
    for page_idx, page in enumerate(pdf.pages):
        print(f"=== PAGE {page_idx + 1} ===")
        words = page.extract_words()
        # Find all description words (x0 around 120-300)
        desc_words = [w for w in words if 115 <= w['x0'] <= 350 and w['top'] >= 180]
        # Group by Y
        lines = {}
        for w in desc_words:
            matched = False
            for y_k in lines:
                if abs(w['top'] - y_k) < 3.0:
                    lines[y_k].append(w)
                    matched = True
                    break
            if not matched:
                lines[w['top']] = [w]
                
        for y_k in sorted(lines.keys()):
            line_str = " ".join([w['text'] for w in sorted(lines[y_k], key=lambda x: x['x0'])])
            x0 = min(w['x0'] for w in lines[y_k])
            x1 = max(w['x1'] for w in lines[y_k])
            print(f"  Y={y_k:.2f} (X={x0:.2f}-{x1:.2f}): {line_str}")
