PDF_PATH = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"

with open(PDF_PATH, "rb") as f:
    pdf_bytes = f.read()

print("PDF length:", len(pdf_bytes))
print("Bytes at 100..500:")
print(pdf_bytes[100:500])

import re
all_startxrefs = list(re.finditer(rb'startxref\s+(\d+)', pdf_bytes))
for m in all_startxrefs:
    print("Found startxref at pos", m.start(), ":", m.group(1).decode())
