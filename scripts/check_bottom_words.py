import pdfplumber

rev_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_sep byk harus revisi.pdf"

with pdfplumber.open(rev_path) as pdf:
    for page_idx in range(len(pdf.pages)):
        page = pdf.pages[page_idx]
        print(f"\n==================== PAGE {page_idx + 1} ====================")
        words = page.extract_words()
        bottom_words = [w for w in words if w['top'] > 715]
        for w in sorted(bottom_words, key=lambda x: (round(x['top'], 1), x['x0'])):
            print(f"  '{w['text']}' at x0={w['x0']:.1f}, top={w['top']:.1f}")
