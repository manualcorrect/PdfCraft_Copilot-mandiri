import zlib
import re

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

m = re.search(rb'\b638\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
dec = zlib.decompress(m.group(2))

gid_to_char = {}
for cid in range(256):
    gid = (dec[cid*2] << 8) | dec[cid*2 + 1]
    if gid != 0:
        gid_to_char[gid] = chr(cid)

for gid in range(1, 73):
    ch = gid_to_char.get(gid, "UNKNOWN")
    print(f"GID {gid:2d}: '{ch}' (ord={ord(ch) if ch!='UNKNOWN' else '?'})")
