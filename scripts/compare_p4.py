import pdfplumber

files = {
    "rev": r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_sep byk harus revisi.pdf",
    "chr": r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026_CHRONOLOGICAL.pdf",
    "orig": r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026.pdf",
    "ref3": r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf",
}

for name, path in files.items():
    print(f"\n==================== FILE: {name} ====================")
    with pdfplumber.open(path) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            words = page.extract_words()
            # print all words that contain "batas" or "akhir" or check page 4
            if page_idx == 3:
                print(f"Page 4 words:")
                for w in words:
                    if w['top'] < 300: # above disclaimer
                        print(f"  {w['text']} at (x0={w['x0']:.1f}, top={w['top']:.1f})")
