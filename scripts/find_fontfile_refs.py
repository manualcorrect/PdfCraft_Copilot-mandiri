import re

with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf", "rb") as f:
    pdf_bytes = f.read()

for m in re.finditer(rb'/FontFile\d?\s+(\d+)\s+0\s+R', pdf_bytes):
    print("FontFile ref:", m.group(0).decode())
