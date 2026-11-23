import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# Let's find each page's content stream
row_pattern = re.compile(
    rb'(q\s+1\s+0\s+0\s+1\s+(?:19\.\d+|20(?:\.0+)?)\s+([\d\.]+)\s+cm\s+BT\s+0\s+0\s+0\s+rg/R1\s+8\s+Tf(/R\d+\s+gs).*?0\.07451\s+0\.294118\s+0\.729412\s+rg/R2\s+8\s+Tf.*?ET\s+Q)',
    re.DOTALL
)

# Find content streams for pages 1..7:
content_oids = [609, 2, 103, 205, 306, 407, 508]

for p_num, c_oid in enumerate(content_oids):
    m = re.search(rb'\b' + str(c_oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    assert m, f"Content stream for Page {p_num+1} (OID {c_oid}) not found"
    dec = zlib.decompress(m.group(2))
    matches = list(row_pattern.finditer(dec))
    print(f"Page {p_num+1} (OID {c_oid}): {len(matches)} row matches found")
    if matches:
        print(f"  First match sample: {matches[0].group(1)[:120]}")
