import re
import zlib
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\test_step3.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

m_startxref = re.search(rb'startxref\s+(\d+)', pdf_bytes)
startxref = int(m_startxref.group(1))
print("PDF length:", len(pdf_bytes), "startxref:", startxref)

# Check XRef stream object
m_xref = re.search(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes[startxref-200:])
if m_xref:
    xref_oid = int(m_xref.group(1))
    print(f"XRef stream OID: {xref_oid}")
    dec_xref = zlib.decompress(m_xref.group(3))
    print(f"Decompressed XRef length: {len(dec_xref)}")

# Check top objects
top_matches = list(re.finditer(rb'(\d+)\s+0\s+obj\b', pdf_bytes))
print(f"Total top objects: {len(top_matches)}")

# Let's find page content streams in test_step3.pdf
page_content_list = []
for m in top_matches:
    oid = int(m.group(1))
    if oid == xref_oid: continue
    # find stream
    m_s = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    if m_s:
        try:
            dec = zlib.decompress(m_s.group(2))
            if b"0.07451 0.294118 0.729412 rg/R2 8 Tf" in dec:
                page_content_list.append(oid)
        except:
            pass

print(f"Discovered page content stream OIDs in test_step3.pdf: {page_content_list}")
