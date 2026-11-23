import sys
sys.path.insert(0, "src")
from pdfcraft_client import PdfCraftClient
import pdfplumber

aug_edited = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_edited ketengangan.pdf"

with pdfplumber.open(aug_edited) as pdf:
    for p_num, page in enumerate(pdf.pages, 1):
        words = page.extract_words()
        base_y = 343.92 if p_num == 1 else 227.92
        wibs = sorted([w for w in words if w['text'] == 'WIB' and w['top'] > 200], key=lambda x: x['top'])
        print(f"\n================ PAGE {p_num} ================")
        for r_i, w in enumerate(wibs):
            row_y = base_y + r_i * 46.00
            row_words = [cw for cw in words if 115 <= cw['x0'] <= 365 and abs(cw['top'] - row_y) < 22]
            lines = {}
            for cw in sorted(row_words, key=lambda x: (x['top'], x['x0'])):
                lines.setdefault(round(cw['top'], 1), []).append(cw['text'])
            first_top = min(lines.keys()) if lines else 0
            first_x0 = min([cw['x0'] for cw in row_words]) if row_words else 0
            print(f"Row {r_i+1:2d} (row_y={row_y:.2f}) | x0={first_x0:.2f} | top={first_top:.2f} (diff={first_top-row_y:+.2f}) | {len(lines)} lines")
            for top, ws in sorted(lines.items()):
                print(f"     top={top:5.1f}: {' '.join(ws)}")
