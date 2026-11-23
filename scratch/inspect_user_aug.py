import pdfplumber

pdf_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\REK_GALANG_AUG.pdf'
with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    for p_idx, page in enumerate(pdf.pages):
        print(f"\n--- PAGE {p_idx+1} ---")
        words = page.extract_words()
        print(f"Total words: {len(words)}")
        hdr_words = [w for w in words if w['top'] < 250]
        print("Header text sample:", " ".join([w['text'] for w in hdr_words[:30]]))
        
        table_words = [w for w in words if w['top'] >= 250]
        wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        print(f"WIB count: {len(wibs)}")
        for w in wibs[:5]:
            row_w = [x['text'] for x in table_words if abs(x['top'] - w['top']) < 12]
            print(f"  Row near y={w['top']:.1f}: {' '.join(row_w)}")

        # Check fonts on this page
        fonts = set(c.get('fontname') for c in page.chars)
        print(f"Fonts on Page {p_idx+1}: {fonts}")
