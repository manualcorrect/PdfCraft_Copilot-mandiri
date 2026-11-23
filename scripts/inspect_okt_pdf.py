import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"
with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages in 0.pdf: {len(pdf.pages)}")
    total_tx = 0
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w['top'] <= 800]
        wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        total_tx += len(wibs)
        
        # page num words
        top_words = [w for w in words if w['top'] < 130 and w['x0'] > 500]
        top_words.sort(key=lambda w: (w['top'], w['x0']))
        pnum_str = " ".join([w['text'] for w in top_words])
        print(f"Page {p_idx+1}: {len(wibs):2d} tx | Header page num: '{pnum_str}'")
    
    print(f"\nTotal transactions across all pages: {total_tx}")
