import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

page_objs = {1: 402, 2: 1, 3: 102, 4: 203, 5: 304}

for p_num, oid in page_objs.items():
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    decomp = zlib.decompress(m.group(2))
    print(f"\n--- Page {p_num} (Obj {oid}) ---")
    for m_s in re.finditer(rb'(\([^\)]*?\))\s*Tj\s*0\.07451\s+0\.294118\s+0\.729412\s+rg/R2\s+8\s+Tf\s*\[\s*(-?\d+)\s*\(([^\)]*?)\)\s*\]TJ', decomp):
        raw_no = m_s.group(1)
        k = m_s.group(2).decode()
        sal = m_s.group(3).decode('utf-16-be', 'ignore')
        # try decoding no
        try:
            clean_no = raw_no[1:-1].decode('utf-16-be')
        except:
            clean_no = str(raw_no)
        print(f"  No={clean_no!r}, K={k}, Saldo={sal}")
