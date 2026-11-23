import pdfplumber

aug_edited = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_edited ketengangan.pdf"
with pdfplumber.open(aug_edited) as pdf:
    for w in pdf.pages[0].extract_words():
        if any(k in w['text'] for k in ['1630', '1650', 'Nomor', 'Account', ':']):
            print(f"{w['text']:<30} x0={w['x0']:.2f}, x1={w['x1']:.2f}, top={w['top']:.2f}")
