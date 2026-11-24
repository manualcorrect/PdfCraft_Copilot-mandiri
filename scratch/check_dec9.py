import re
import zlib

pdf_path = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\scratch\test_desc_edit.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

sx_matches = re.findall(rb"startxref[\r\n]+(\d+)", pdf_bytes)
xref_offset = int(sx_matches[-1])

m_xref = re.search(rb"\b(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream", pdf_bytes[xref_offset-50:], re.DOTALL)
xref_dict = m_xref.group(2)
xref_stream = m_xref.group(3)
decomp_xref = zlib.decompress(xref_stream)

# Get OID 9
m_9 = re.search(rb"\b9\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream", pdf_bytes, re.DOTALL)
dec9 = zlib.decompress(m_9.group(2)).decode("latin1", errors="ignore")

pos_c1 = dec9.find("446.12 667")
print("pos_c1:", pos_c1)
pos_c4 = dec9.find("446.12 597")
print("pos_c4:", pos_c4)
pos_now = dec9.find("16 676 cm")
print("pos_now:", pos_now)
