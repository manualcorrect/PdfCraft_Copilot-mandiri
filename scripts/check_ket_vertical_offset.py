import pdfplumber

ref_2 = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"

with pdfplumber.open(ref_2) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w['top'] <= 800]
        wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        print(f"\n--- Page {p_idx+1} ---")
        base_y = 343.92 if p_idx == 0 else 227.92
        for r_i, w in enumerate(wibs):
            expected_row_y = base_y + r_i * 46.00
            # find first word of keterangan in this row
            ket_words = [cw for cw in table_words if 115 <= cw['x0'] <= 365 and abs(cw['top'] - w['top']) < 22]
            if ket_words:
                top_word = min(ket_words, key=lambda x: x['top'])
                print(f"Row {r_i+1:2d} | expected_row_y={expected_row_y:.2f} | first_ket_top={top_word['top']:.2f} | diff={(top_word['top'] - expected_row_y):.2f} | text='{top_word['text']}'")
