import re

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

for oid in [599, 600, 601, 602, 603, 604, 605, 606, 607, 608]:
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>', pdf_bytes)
    if m:
        print(f"Obj {oid}: {m.group(1).decode('latin1', 'ignore')[:100]}")
