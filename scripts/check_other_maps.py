import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# Find all CIDToGIDMap objects
for m in re.finditer(rb'/CIDToGIDMap\s+(\d+)\s+0\s+R', pdf_bytes):
    print("Found CIDToGIDMap ref:", m.group(0).decode())

# Check objects 641, 644 etc
for oid in [638, 641, 644]:
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    if m:
        dec = zlib.decompress(m.group(2))
        cid_c = ord('c')
        gid_c = (dec[cid_c*2] << 8) | dec[cid_c*2 + 1]
        print(f"Map {oid}: 'c' -> GID {gid_c}")
