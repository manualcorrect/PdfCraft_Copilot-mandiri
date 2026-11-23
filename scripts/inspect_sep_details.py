import re
import zlib
import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# Find pages catalog and page objects
page_matches = list(re.finditer(rb'(\d+)\s+0\s+obj\s*<<(?:(?!endobj).)*?/Type\s*/Page\b(?:(?!endobj).)*?>>\s*endobj', pdf_bytes, re.DOTALL))
print("Found /Type /Page count in 0.pdf:", len(page_matches))
content_oids = []
for idx, pm in enumerate(page_matches):
    p_oid = int(pm.group(1))
    p_text = pm.group(0).decode('latin1', errors='ignore')
    m_contents = re.search(r'/Contents\s+(\d+)\s+0\s+R', p_text)
    if m_contents:
        c_oid = int(m_contents.group(1))
        content_oids.append(c_oid)
        print(f"Page {idx+1} (OID {p_oid}): /Contents {c_oid}")

print(f"Content OIDs: {content_oids}")

# Inspect Page 1 content stream
p1_raw_m = re.search(rb'\b' + str(content_oids[0]).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
if p1_raw_m:
    p1_decomp = zlib.decompress(p1_raw_m.group(2)).decode('latin1', errors='ignore')
    pos_c1 = p1_decomp.find('446.12 667')
    pos_c4 = p1_decomp.find('446.12 597')
    print(f"Page 1 Summary Box: pos_c1={pos_c1}, pos_c4={pos_c4}")
    pos_now = p1_decomp.find('16 676 cm')
    print(f"pos_now={pos_now}")
    matches_b2 = list(re.finditer(r'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+667\s+cm', p1_decomp))
    print(f"matches_b2 len: {len(matches_b2)}")
    if matches_b2:
        print("Slice of b2:")
        print(p1_decomp[matches_b2[0].start() : matches_b2[0].start() + 250])
