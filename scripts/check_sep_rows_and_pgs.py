import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

row_pattern = re.compile(
    rb'(q\s+1\s+0\s+0\s+1\s+(?:19\.\d+|20(?:\.0+)?)\s+([\d\.]+)\s+cm\s+BT\s+0\s+0\s+0\s+rg/R1\s+8\s+Tf(/R\d+\s+gs).*?0\.07451\s+0\.294118\s+0\.729412\s+rg/R2\s+8\s+Tf.*?ET\s+Q)',
    re.DOTALL
)

content_oids = [647, 2, 103, 204, 305, 406, 507]
for idx, c_oid in enumerate(content_oids):
    p_num = idx + 1
    m = re.search(rb'\b' + str(c_oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    assert m, f"Page {p_num} (OID {c_oid}) not found"
    dec = zlib.decompress(m.group(2))
    matches = list(row_pattern.finditer(dec))
    print(f"Page {p_num} (OID {c_oid}): {len(matches)} row matches")
    
    # check page numbers blocks
    m_it = re.search(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+726\s+cm\s+BT\s+0\s+0\s+0\s+rg/R3\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', dec, re.DOTALL)
    bold_blocks = list(re.finditer(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+736\s+cm\s+BT\s+0\s+0\s+0\s+rg/R2\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', dec, re.DOTALL))
    print(f"  m_it found? {m_it is not None} | bold_blocks: {len(bold_blocks)}")
