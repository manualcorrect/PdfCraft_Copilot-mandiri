import zlib
import re

def parse_xref_stream(pdf_bytes):
    # Find startxref
    sx_matches = re.findall(rb'startxref[\r\n]+(\d+)', pdf_bytes)
    assert sx_matches, "startxref not found"
    xref_offset = int(sx_matches[-1])
    
    # Extract xref stream obj
    m_xref = re.search(rb'\b(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes[xref_offset-50:], re.DOTALL)
    assert m_xref, f"Xref object not found near offset {xref_offset}"
    
    xref_oid = int(m_xref.group(1))
    xref_dict = m_xref.group(2)
    xref_stream = m_xref.group(3)
    
    # Check /Size and /W
    m_size = re.search(r'/Size\s+(\d+)', xref_dict.decode('latin1'))
    size = int(m_size.group(1))
    
    m_w = re.search(r'/W\s*\[\s*(\d+)\s+(\d+)\s+(\d+)\s*\]', xref_dict.decode('latin1'))
    w1, w2, w3 = int(m_w.group(1)), int(m_w.group(2)), int(m_w.group(3))
    cols = w1 + w2 + w3
    stride = cols + 1
    
    decomp = zlib.decompress(xref_stream)
    
    rows = []
    prev = bytearray(cols)
    for i in range(size):
        row_bytes = decomp[i*stride : (i+1)*stride]
        filter_type = row_bytes[0]
        curr = bytearray(row_bytes[1:])
        if filter_type == 2: # PNG Up filter
            for c in range(cols):
                curr[c] = (curr[c] + prev[c]) % 256
        prev = curr
        
        # parse w1, w2, w3
        f1 = curr[0] if w1 == 1 else 0
        f2 = (curr[w1] << 8) | curr[w1+1] if w2 == 2 else curr[w1]
        f3 = (curr[w1+w2] << 8) | curr[w1+w2+1] if w3 == 2 else curr[w1+w2]
        rows.append([f1, f2, f3])
        
    return xref_oid, xref_dict, rows

for label, p in [('AUG', 'output/REK_KEISYA_AUG_OUTPUT_1.pdf'), ('SEP', 'output/REK_KEISYA_SEP_OUTPUT_1.pdf'), ('OKT', 'output/REK_KEISYA_OKT_OUTPUT_1.pdf')]:
    with open(p, 'rb') as f:
        data = f.read()
    xid, xdict, rows = parse_xref_stream(data)
    print(f"{label}: XRef obj {xid}, {len(rows)} entries")
    # print first 5 objects
    for i in range(1, 15):
        if rows[i][0] == 1:
            print(f"  Obj {i}: offset {rows[i][1]}")
