import re
import zlib

sep_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"
with open(sep_pdf, "rb") as f:
    b = f.read()

for oid in [393, 396]:
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL)
    print(f"SEP Obj {oid} dict: {m.group(1)}")
    dec = zlib.decompress(m.group(2))
    print(f"SEP Obj {oid} decomp len: {len(dec)}")
    print(dec[:300])
