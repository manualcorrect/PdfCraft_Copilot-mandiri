import pdfplumber

def check_fonts(pdf_path):
    print("=== Checking:", pdf_path)
    with pdfplumber.open(pdf_path) as pdf:
        for p_idx, page in enumerate(pdf.pages):
            words = page.extract_words(extra_attrs=['fontname', 'size'])
            for w in words:
                if any(k in w['text'] for k in ['Jan', 'Sep', 'Oct', 'Taman', 'Ciceri', 'GALANG', 'ROY']):
                    print(f"P{p_idx+1} {w['text']:20s} font={w['fontname']} size={w['size']}")

check_fonts(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf")
check_fonts("output/REK_GALANG_OCT_2026_CHRONOLOGICAL.pdf")
