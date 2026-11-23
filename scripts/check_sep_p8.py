import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf") as pdf:
    p8 = pdf.pages[7]
    print("Page 8 text:")
    print(p8.extract_text())
    print("\nPage 7 text (last 300 characters):")
    print(pdf.pages[6].extract_text()[-300:])
