import re
import zlib

pdf_path = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\scratch\test_desc_edit.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

for oid in [9, 112, 212]:
    m = re.search(rb"\b" + str(oid).encode() + rb"\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream", pdf_bytes, re.DOTALL)
    dec = zlib.decompress(m.group(2))
    m_it = re.search(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+726\s+cm\s+BT\s+0\s+0\s+0\s+rg/R3\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', dec, re.DOTALL)
    m_b = list(re.finditer(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+736\s+cm\s+BT\s+0\s+0\s+0\s+rg/R2\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', dec, re.DOTALL))
    print(f"OID {oid:3d}: m_it found={m_it is not None}, m_b count={len(m_b)}")
