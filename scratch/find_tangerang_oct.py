import pdfplumber

with pdfplumber.open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\REK_GALANG_OCT_2026_PERFECT.pdf') as pdf:
    for p_idx, p in enumerate(pdf.pages):
        words = p.extract_words()
        for w in words:
            if 'TANGERANG' in w['text']:
                print(f"Found TANGERANG on P{p_idx+1}: {w}")
