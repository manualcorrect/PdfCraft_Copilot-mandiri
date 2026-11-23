import pdfplumber
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

nasih_path = r"D:\X_Files\rekening\Reference\nasih 2024 new unlocked\ilovepdf_unlocked\e-Statement_XXXXXXXXX9210_01 Des 2024-31 Des 2024_unlocked.pdf"
roy_agu = r"D:\X_Files\rekening\Reference\Roy\ilovepdf_unlocked\Agu 2026_unlocked.pdf"
roy_mei = r"D:\X_Files\rekening\Reference\Roy\ilovepdf_unlocked\Mei 2026_unlocked.pdf"

docs = [("Nasih Des 2024", nasih_path), ("Roy Agu 2026", roy_agu), ("Roy Mei 2026", roy_mei)]

for doc_name, path in docs:
    print(f"\n==================== {doc_name} ====================")
    with pdfplumber.open(path) as pdf:
        all_descs = []
        for p_idx, page in enumerate(pdf.pages[:3]): # check first 3 pages
            words = page.extract_words()
            min_y = 320 if p_idx == 0 else 200
            # Table words in keterangan column: 120 <= x0 <= 360
            desc_words = [w for w in words if min_y <= w['top'] <= 800 and 120 <= w['x0'] <= 360]
            # Group by vertical position or row
            # Let's inspect paragraphs or lines
        
        # Let's use PdfCraft client or pdfplumber to get text of descriptions
        # In pdfplumber, let's extract words grouped by row Y
        page1 = pdf.pages[0]
        words_p1 = [w for w in page1.extract_words() if 320 <= w['top'] <= 800 and 120 <= w['x0'] <= 360]
        # Group into lines by top (within 4 pt)
        from itertools import groupby
        sorted_words = sorted(words_p1, key=lambda w: w['top'])
        lines = []
        for _, g in groupby(sorted_words, key=lambda w: round(w['top'] / 8.0) * 8.0):
            line_words = sorted(list(g), key=lambda w: w['x0'])
            line_str = " ".join(w['text'] for w in line_words)
            y_avg = sum(w['top'] for w in line_words) / len(line_words)
            lines.append((y_avg, line_str, line_words[0]['x0'], line_words[-1]['x1']))
            
        print("Page 1 Description lines:")
        for y, l, x0, x1 in lines[:15]:
            w_box = x1 - x0
            print(f"  y={y:5.1f} | x0={x0:5.1f} x1={x1:5.1f} (w={w_box:5.1f}) | {l}")
