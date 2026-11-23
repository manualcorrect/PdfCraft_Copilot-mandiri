import pdfplumber

pdf_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\REK_GALANG_AUG.pdf'

print("=== DETAILED AUDIT OF USER'S MANUAL REK_GALANG_AUG.pdf ===")
with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        print(f"\n--- PAGE {p_idx+1} ---")
        hdr = [w['text'] for w in sorted([w for w in words if w['top'] < 130], key=lambda x: (x['top'], x['x0']))]
        print(f"Header: {' '.join(hdr[:25])}")
        
        if p_idx == 0:
            sm = [f"{w['text']} (y={w['top']:.1f}, x={w['x0']:.1f})" for w in sorted([w for w in words if 140 <= w['top'] <= 250 and w['x0'] > 450], key=lambda x: x['top'])]
            print(f"Summary values: {sm}")

        wibs = sorted([w for w in words if w['text'] == 'WIB'], key=lambda x: x['top'])
        print(f"Total transactions on page: {len(wibs)}")
        for i, w in enumerate(wibs):
            row_words = [x['text'] for x in sorted([x for x in words if abs(x['top'] - w['top']) < 15 and x['top'] >= 250], key=lambda x: x['x0'])]
            print(f"  Row {i+1} (y={w['top']:.1f}): {' '.join(row_words)}")

        fonts = set(c.get('fontname') for c in page.chars)
        print(f"Fonts on Page {p_idx+1}: {fonts}")
