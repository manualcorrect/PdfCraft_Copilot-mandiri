import pdfplumber

sep_rev = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_sep byk harus revisi.pdf"
sep_ref = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\3.pdf"
sep_chrono = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_SEP_2026_CHRONOLOGICAL.pdf"

print("--- EXAMINING REK_GALANG_sep byk harus revisi.pdf ---")
with pdfplumber.open(sep_rev) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    for i, p in enumerate(pdf.pages, 1):
        print(f"\n--- Page {i} ---")
        # Check text length
        text = p.extract_text() or ""
        print(f"Text length: {len(text)}")
        words = p.extract_words()
        print(f"Words count: {len(words)}")
        # Check if there are annotations or drawings or comments
        annots = p.annots or []
        print(f"Annotations count: {len(annots)}")
        for a in annots:
            print(f"  Annot: type={a.get('type')}, rect={a.get('rect')}, contents={repr(a.get('contents', ''))}")
