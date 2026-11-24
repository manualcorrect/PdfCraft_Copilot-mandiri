pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

print("File size:", len(pdf_bytes))
print("Last 500 bytes:")
print(pdf_bytes[-500:])
