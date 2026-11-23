import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

for oid, name in {393: "Regular", 396: "Bold", 399: "Italic"}.items():
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    decomp = zlib.decompress(m.group(2))
    print(f"\nCIDToGIDMap {name} (Obj {oid}) len={len(decomp)} (maps {len(decomp)//2} CIDs):")
    for d in "0123456789":
        cid = ord(d)
        if (cid + 1) * 2 <= len(decomp):
            gid = (decomp[cid*2] << 8) | decomp[cid*2 + 1]
            print(f"  CID '{d}' ({cid}) -> GID {gid}")
        else:
            print(f"  CID '{d}' ({cid}) -> OUT OF RANGE")
