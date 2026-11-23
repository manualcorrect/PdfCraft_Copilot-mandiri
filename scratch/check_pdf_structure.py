with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf", "rb") as f:
    data = f.read()

print("File size:", len(data))
print("Header:", data[:50])
print("Trailer area:", data[-500:])
