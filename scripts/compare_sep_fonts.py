with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf", "rb") as f:
    b_k = f.read()

with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf", "rb") as f:
    b_i = f.read()

import re
print("Keisya Sep fonts in 0.pdf:")
for m in re.finditer(rb'/BaseFont\s*/([^\s>]+)', b_k):
    print("  ", m.group(1).decode())

print("\nIbnu Sep fonts in 0.pdf:")
for m in re.finditer(rb'/BaseFont\s*/([^\s>]+)', b_i):
    print("  ", m.group(1).decode())
