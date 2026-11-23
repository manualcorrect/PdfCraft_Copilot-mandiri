import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

m = re.search(rb'\b638\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
if m:
    dec = zlib.decompress(m.group(2))
    print(f"CIDToGIDMap 638 length: {len(dec)} bytes")
    # check CID 99 (offset 99*2 = 198)
    cid_c = ord('c')
    gid_c = (dec[cid_c*2] << 8) | dec[cid_c*2 + 1]
    print(f"CID for 'c' (99) -> GID: {gid_c}")
    for ch in ['C', 'i', 'c', 'e', 'r']:
        cid = ord(ch)
        gid = (dec[cid*2] << 8) | dec[cid*2 + 1]
        print(f"Char '{ch}' (CID {cid}) -> GID {gid}")
