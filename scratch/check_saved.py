import re
import zlib

pdf_path = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\scratch\test_wafiq.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

sx_matches = re.findall(rb"startxref[\r\n]+(\d+)", pdf_bytes)
print("startxref matches:", sx_matches)
xref_offset = int(sx_matches[-1])
print("XRef offset:", xref_offset)
print("Bytes at offset:", pdf_bytes[xref_offset:xref_offset+100])
