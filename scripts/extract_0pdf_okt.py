import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\okt\0.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for p_idx, page in enumerate(pdf.pages):
        print(f"\n--- PAGE {p_idx+1} ---")
        text = page.extract_text()
        lines = text.splitlines()
        for l in lines:
            # print lines that start with a digit or contain WIB or contain - or +
            if any(term in l for term in ['WIB', 'May 2026', 'Oct 2026', 'Saldo (IDR)', 'Nominal (IDR)']):
                print(l[:80])
            elif l and l.split()[0].isdigit() and len(l.split()[0]) <= 3:
                print(l[:80])
