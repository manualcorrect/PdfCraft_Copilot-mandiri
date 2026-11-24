import pdfplumber

with pdfplumber.open(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\sep\0.pdf') as pdf:
    p5 = pdf.pages[4]
    print("=== Page 5 Text ===")
    print(p5.extract_text())
