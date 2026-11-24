import re
import zlib

pdf_path = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\scratch\test_desc_edit.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

row_pattern = re.compile(
    rb'(q\s+1\s+0\s+0\s+1\s+(?:19\.\d+|20(?:\.0+)?)\s+([\d\.]+)\s+cm\s+BT\s+0\s+0\s+0\s+rg/R1\s+8\s+Tf(/R\d+\s+gs).*?0\.07451\s+0\.294118\s+0\.729412\s+rg/R2\s+8\s+Tf.*?ET\s+Q)',
    re.DOTALL
)

for p_num, oid in enumerate([9, 112, 212], 1):
    m = re.search(rb"\b" + str(oid).encode() + rb"\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream", pdf_bytes, re.DOTALL)
    dec = zlib.decompress(m.group(2))
    matches = list(row_pattern.finditer(dec))
    print(f"Page {p_num} (OID {oid}): matched {len(matches)} rows")
