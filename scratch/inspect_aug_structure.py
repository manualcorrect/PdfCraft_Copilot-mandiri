import pdfplumber

pdf_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\REK_GALANG_AUG.pdf'
with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        print(f"\n==================== PAGE {p_idx+1} ====================")
        words = page.extract_words()
        # Find all No
        nos = [w for w in words if w['x0'] < 45 and w['top'] > 300 and w['text'].isdigit()]
        wibs = [w for w in words if w['text'] == 'WIB']
        print(f"Total numbers in No column: {len(nos)}: {[w['text'] for w in nos]}")
        print(f"Total WIB: {len(wibs)}")
        
        # Check first 3 rows in detail
        for no_w in nos[:3]:
            row_words = [w for w in words if abs(w['top'] - no_w['top']) < 15]
            print(f"  Row {no_w['text']}: top={no_w['top']:.1f}, words={[w['text'] for w in sorted(row_words, key=lambda x: x['x0'])]}")
