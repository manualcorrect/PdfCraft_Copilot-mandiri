pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\okt\0.pdf"
with open(pdf_path, 'rb') as f:
    b = f.read()

print("Last 500 bytes of 0.pdf:")
print(b[-500:].decode('latin1', errors='ignore'))
