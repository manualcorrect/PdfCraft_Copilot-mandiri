import re
import zlib
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

def get_stream(oid):
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    return zlib.decompress(m.group(2))

for oid in [542, 545, 548]:
    s = get_stream(oid)
    print(f"--- OBJ {oid} (len {len(s)}) ---")
    print(s.decode('latin1', errors='ignore')[:300])
