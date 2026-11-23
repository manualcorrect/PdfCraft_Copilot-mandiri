import re

with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf", "rb") as f:
    data = f.read()

# Find all obj
objs = re.findall(rb'(\d+)\s+(\d+)\s+obj', data)
print(f"Total objects found: {len(objs)}")
print("First 10 objects:", objs[:10])
