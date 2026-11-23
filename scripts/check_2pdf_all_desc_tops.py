import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from pdfcraft_client import PdfCraftClient
import pdfplumber

# Let's inspect all 10 descriptions on Page 1 of 2.pdf to get their exact top coordinates
print("=== 2.pdf Page 1 Authentic Description Tops ===")
with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf") as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    # for each of the 10 rows
    for r in range(1, 11):
        # find the description words for this row
        # row centers are roughly 344, 390, 436, 482, 528, 574, 620, 666, 712, 758
        row_y = 343.92 + (r - 1) * 46.00
        desc_w = sorted([w for w in words if abs(w['top'] - row_y) < 22 and 120 <= w['x0'] <= 365], key=lambda x: (x['top'], x['x0']))
        # group by top
        lines = {}
        for w in desc_w:
            lines.setdefault(round(w['top'], 1), []).append(w['text'])
        print(f"Row {r:02d} (row_y={row_y:.2f}):")
        for top in sorted(lines.keys()):
            print(f"    top={top:5.1f}: {' '.join(lines[top])}")
