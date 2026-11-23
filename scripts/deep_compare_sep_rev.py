import pdfplumber

sep_rev = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_sep byk harus revisi.pdf"
sep_ref = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"
sep_chrono = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026_CHRONOLOGICAL.pdf"
sep_orig = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026.pdf"

print("==================================================")
print("COMPARING REK_GALANG_sep byk harus revisi.pdf")
print("==================================================")

with pdfplumber.open(sep_rev) as p_rev, pdfplumber.open(sep_ref) as p_ref, pdfplumber.open(sep_chrono) as p_chr:
    for page_idx in range(len(p_rev.pages)):
        print(f"\n==================== PAGE {page_idx + 1} ====================")
        page_rev = p_rev.pages[page_idx]
        page_chr = p_chr.pages[page_idx]
        page_ref = p_ref.pages[page_idx]
        
        text_rev = page_rev.extract_text() or ""
        text_chr = page_chr.extract_text() or ""
        
        lines_rev = [l.strip() for l in text_rev.split("\n") if l.strip()]
        lines_chr = [l.strip() for l in text_chr.split("\n") if l.strip()]
        
        print(f"Lines count: rev={len(lines_rev)}, chrono={len(lines_chr)}")
        
        # Print lines of rev
        print("--- REV LINES ---")
        for i, l in enumerate(lines_rev):
            print(f"{i:2d}: {l}")
