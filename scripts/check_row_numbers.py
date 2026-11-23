import pdfplumber

rev_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_sep byk harus revisi.pdf"

with pdfplumber.open(rev_path) as pdf:
    for page_idx, page in enumerate(pdf.pages, 1):
        print(f"\n==================== PAGE {page_idx} ====================")
        words = page.extract_words()
        # Find all numbers that look like row numbers (1 to 35)
        # In Mandiri statements, row numbers are at x0 approx 20.0
        row_num_words = [w for w in words if w['text'].isdigit() and 1 <= int(w['text']) <= 35 and w['top'] > 200 and w['top'] < 720]
        # Filter for those near x0 ~ 20
        print("Candidate row numbers:")
        for w in sorted(row_num_words, key=lambda x: x['top']):
            print(f"  No {w['text']} at x0={w['x0']:.1f}, top={w['top']:.1f}")
