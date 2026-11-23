import re

aug_out_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\REK_KEISYA_AUG_OUTPUT_1.pdf"

with open(aug_out_pdf, "rb") as f:
    b = f.read()

for m in re.finditer(rb'/Font\s*<<(.*?)>>', b, re.DOTALL):
    print("Found /Font dict:", m.group(1).decode('latin1', errors='ignore')[:200])
