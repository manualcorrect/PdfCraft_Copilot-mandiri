import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        # header right words
        header_right = [w for w in words if w['x0'] > 500 and w['top'] < 130]
        print(f"Page {p_idx+1} header right words:")
        for w in header_right:
            print(f"  '{w['text']}' top={w['top']:.2f}, bottom={w['bottom']:.2f}, x0={w['x0']:.2f}, x1={w['x1']:.2f}")
