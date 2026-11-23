import pdfplumber

sep_rev = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\SEP\REK_GALANG_sep byk harus revisi.pdf"

with pdfplumber.open(sep_rev) as pdf:
    for page_idx, page in enumerate(pdf.pages, 1):
        foreign_chars = [c for c in page.chars if 'TTInterphases' not in c.get('fontname', '')]
        if foreign_chars:
            print(f"\n--- Page {page_idx} Foreign Font Characters ({len(foreign_chars)}) ---")
            # Group by font and print sample text
            by_font = {}
            for c in foreign_chars:
                by_font.setdefault(c.get('fontname'), []).append(c)
            for fn, chars in by_font.items():
                text = "".join(c['text'] for c in sorted(chars, key=lambda x: (round(x['top'], 1), x['x0'])))
                print(f"Font '{fn}': count={len(chars)}, text='{text}'")
                for c in chars[:5]:
                    print(f"  sample: char='{c['text']}', x0={c['x0']:.1f}, top={c['top']:.1f}, size={c['size']:.1f}")
