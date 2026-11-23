import zlib, re

with open('output/REK_IBNU_OKT_OUTPUT_1.pdf', 'rb') as f:
    pdf_bytes = f.read()

page_oids = [12, 115, 214, 314, 413, 513]
for p_idx, oid in enumerate(page_oids):
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    dec = zlib.decompress(m.group(2))
    
    # Italic block
    m_it = re.search(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+726\s+cm\s+BT\s+0\s+0\s+0\s+rg/R3\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', dec, re.DOTALL)
    # Bold blocks
    bold_blocks = list(re.finditer(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+736\s+cm\s+BT\s+0\s+0\s+0\s+rg/R2\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', dec, re.DOTALL))
    
    print(f"Page {p_idx+1} (OID {oid}): m_it={'FOUND' if m_it else 'MISSING'}, bold_blocks={len(bold_blocks)}")
    if m_it:
        print(f"  m_it text: {m_it.group(0)[:60]}")
    for bb in bold_blocks:
        print(f"  bold text: {bb.group(0)[:60]}")
