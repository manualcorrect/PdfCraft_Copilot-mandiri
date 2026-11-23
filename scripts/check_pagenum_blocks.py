import re
import zlib

with open("output/REK_IBNU_AUG_OUTPUT_1.pdf", "rb") as f:
    pdf_bytes = f.read()

page_content_list = [12, 114, 213, 313, 412, 511, 610]
for idx, oid in enumerate(page_content_list):
    p_num = idx + 1
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    dec = zlib.decompress(m.group(2))
    
    m_it = re.search(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+726\s+cm\s+BT\s+0\s+0\s+0\s+rg/R3\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', dec, re.DOTALL)
    bold_blocks = list(re.finditer(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+736\s+cm\s+BT\s+0\s+0\s+0\s+rg/R2\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', dec, re.DOTALL))
    print(f"Page {p_num} (OID {oid}): m_it found? {m_it is not None} | bold_blocks count: {len(bold_blocks)}")
