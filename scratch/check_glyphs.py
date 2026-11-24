import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf"
chars = set()
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        txt = page.extract_text() or ""
        chars.update(set(txt))

needed = set("WAFIQ DWI ANANDA KCP Serang Ciceri 01 Aug 2026 - 31 Aug 2026 22 Nov 2026 1630016689138 + 5.900.000,00 - 8.068.801,00 2.615.994,81 5.500.000,00 450.000,00 5.000,00 PT BENDI NASHA NIAGA INDUSTRI 5411078192 (CENAIDJA) Biaya administrasi rekening 4 dari 4 4 of 4")

missing = needed - chars
print("Needed characters missing from 0.pdf:", missing)
