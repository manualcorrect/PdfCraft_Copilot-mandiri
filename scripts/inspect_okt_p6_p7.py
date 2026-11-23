import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"
with pdfplumber.open(pdf_path) as pdf:
    print("=== Page 6 Text ===")
    print(pdf.pages[5].extract_text()[:400])
    print("\n=== Page 7 Text ===")
    print(pdf.pages[6].extract_text())
