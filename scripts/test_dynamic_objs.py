import re
import zlib

def test_dynamic_top_objs(pdf_path, name):
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()

    # Find startxref
    sx_matches = re.findall(rb'startxref[\r\n]+(\d+)', pdf_bytes)
    xref_offset = int(sx_matches[-1])
    
    m_xref = re.search(rb'\b(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes[xref_offset-50:], re.DOTALL)
    xref_oid = int(m_xref.group(1))
    xref_dict = m_xref.group(2)
    xref_stream = m_xref.group(3)
    
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
        if filter_type == 2:
            for c in range(cols):
                curr[c] = (curr[c] + prev[c]) % 256
        prev = curr
        f1 = curr[0] if w1 == 1 else 0
        f2 = (curr[w1] << 8) | curr[w1+1] if w2 == 2 else curr[w1]
        f3 = (curr[w1+w2] << 8) | curr[w1+w2+1] if w3 == 2 else curr[w1+w2]
        rows.append([f1, f2, f3])

    # Find all type 1 objects (excluding xref_oid itself)
    top_objs = [i for i in range(size) if rows[i][0] == 1 and i != xref_oid]
    top_objs.sort(key=lambda oid: rows[oid][1])
    
    print(f"\n{name} top_objs ({len(top_objs)}): {top_objs}")
    # Verify each offset points to '{oid} 0 obj'
    for oid in top_objs:
        off = rows[oid][1]
        token = f"{oid} 0 obj".encode()
        actual = pdf_bytes[off:off+len(token)]
        assert actual == token, f"Mismatch at oid {oid}, off {off}: {actual} != {token}"
    print(f"All {len(top_objs)} object offsets verified successfully in {name}!")

test_dynamic_top_objs('output/REK_KEISYA_AUG_OUTPUT_1.pdf', 'AUG')
test_dynamic_top_objs('output/REK_KEISYA_SEP_OUTPUT_1.pdf', 'SEP')
test_dynamic_top_objs('output/REK_KEISYA_OKT_OUTPUT_1.pdf', 'OKT')
