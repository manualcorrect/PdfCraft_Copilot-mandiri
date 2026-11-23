import pdfplumber

sep_rev = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_sep byk harus revisi.pdf"
sep_ref = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"

print("--- FONTS IN REV ---")
with pdfplumber.open(sep_rev) as pdf:
    for page_idx, page in enumerate(pdf.pages, 1):
        fonts = set(c.get('fontname') for c in page.chars)
        print(f"Page {page_idx} fonts: {fonts}")

print("\n--- FONTS IN REF (3.pdf) ---")
with pdfplumber.open(sep_ref) as pdf:
    for page_idx, page in enumerate(pdf.pages, 1):
        fonts = set(c.get('fontname') for c in page.chars)
        print(f"Page {page_idx} fonts: {fonts}")

print("\n--- CHECKING KETERANGAN COORDS IN REV ---")
with pdfplumber.open(sep_rev) as pdf:
    for page_idx, page in enumerate(pdf.pages, 1):
        words = page.extract_words()
        no_words = [w for w in words if abs(w['x0'] - 20.0) < 5 and 200 < w['top'] < 780 and w['text'].isdigit()]
        no_words.sort(key=lambda w: w['top'])
        for nw in no_words:
            no_val = int(nw['text'])
            y = nw['top']
            ket_words = [w for w in words if 118 <= w['x0'] < 360 and abs(w['top'] - y) < 16]
            if ket_words:
                min_x0 = min(w['x0'] for w in ket_words)
                min_top = min(w['top'] for w in ket_words)
                max_bottom = max(w['bottom'] for w in ket_words)
                print(f"Row {no_val:2d} (P{page_idx}) row_y={y:.1f}: min_x0={min_x0:.2f}, min_top={min_top:.2f}, span_h={max_bottom-min_top:.2f}")
