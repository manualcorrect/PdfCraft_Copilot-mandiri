import re
import zlib

pdf_path = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\scratch\test_wafiq_step3.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

sx_matches = re.findall(rb"startxref[\r\n]+(\d+)", pdf_bytes)
xref_offset = int(sx_matches[-1])
print("XRef offset:", xref_offset)
print(pdf_bytes[xref_offset:])

m_xref = re.search(rb"\b(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream", pdf_bytes[xref_offset:], re.DOTALL)
if m_xref:
    print("Matched XRef obj:", m_xref.group(1))
    print("XRef dict:", m_xref.group(2))
    decomp = zlib.decompress(m_xref.group(3))
    print("Decompressed xref length:", len(decomp))
else:
    print("Xref is table, not stream. Let's check table format.")
    print(pdf_bytes[xref_offset:xref_offset+300])
