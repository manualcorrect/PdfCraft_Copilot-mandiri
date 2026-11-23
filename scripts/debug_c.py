import re, zlib

with open('output/REK_IBNU_SEP_OUTPUT_1.pdf', 'rb') as f:
    b = f.read()

# find /Type /Page
m_pages = list(re.finditer(rb'<<[^\>]*?/Type\s*/Page\b[^\>]*?>>', b))
print(f"Total pages: {len(m_pages)}")
p1_dict = m_pages[0].group(0).decode('latin1')
print("P1 dict:", p1_dict)

m_cnt = re.search(r'/Contents\s+(\d+)\s+0\s+R', p1_dict)
if not m_cnt:
    m_cnt = re.search(r'/Contents\s*\[\s*(\d+)', p1_dict)
cnt_oid = int(m_cnt.group(1))
print("Contents OID:", cnt_oid)

m_stream = re.search(rb'\b' + str(cnt_oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL)
if m_stream:
    dec = zlib.decompress(m_stream.group(2))
    print(f"P1 contents length: {len(dec)}")
    # Find any text around y=120..140 or BT..ET
    # Let's search for 167 or 139 or 122
    for l in dec.splitlines():
        if any(term in l for term in [b'122', b'139', b'167', b'KCP', b'Branch', b'Cabang']):
            print(l)
