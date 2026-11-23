import pdfplumber
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\REK GALANG JUL 2026.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for p_idx in [0, 1]:
        page = pdf.pages[p_idx]
        print(f"=== PAGE {p_idx+1} TRANSACTIONS DUMP ===")
        min_y = 320 if p_idx == 0 else 200
        words = [w for w in page.extract_words() if min_y <= w["top"] <= 800]
        # Group words by approx vertical line (top within 3 pt)
        lines = {}
        for w in words:
            # find closest line top
            matched_top = None
            for top in lines:
                if abs(top - w["top"]) < 4.0:
                    matched_top = top
                    break
            if matched_top is None:
                matched_top = w["top"]
                lines[matched_top] = []
            lines[matched_top].append(w)
        
        sorted_tops = sorted(lines.keys())
        for top in sorted_tops:
            line_words = sorted(lines[top], key=lambda x: x["x0"])
            line_str = " ".join(w["text"] for w in line_words)
            print(f"y={top:6.2f} | {line_str}")
