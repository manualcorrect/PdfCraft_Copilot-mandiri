import os
import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

sx_matches = re.findall(rb"startxref[\r\n]+(\d+)", pdf_bytes)
xref_offset = int(sx_matches[-1])
print("XRef offset:", xref_offset)

m_xref = re.search(rb"\b(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream", pdf_bytes[xref_offset-50:], re.DOTALL)
xref_oid = int(m_xref.group(1))
xref_dict = m_xref.group(2)
xref_stream = m_xref.group(3)
print("XRef OID:", xref_oid)

m_size = re.search(r"/Size\s+(\d+)", xref_dict.decode("latin1"))
size = int(m_size.group(1))
m_w = re.search(r"/W\s*\[\s*(\d+)\s+(\d+)\s+(\d+)\s*\]", xref_dict.decode("latin1"))
w1, w2, w3 = int(m_w.group(1)), int(m_w.group(2)), int(m_w.group(3))
cols = w1 + w2 + w3
stride = cols + 1
decomp_xref = zlib.decompress(xref_stream)

rows = []
prev = bytearray(cols)
for i in range(size):
    row_bytes = decomp_xref[i*stride : (i+1)*stride]
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

top_objs = [i for i in range(size) if rows[i][0] == 1 and i != xref_oid]
top_objs.sort(key=lambda oid: rows[oid][1])

obj_raw = {}
for i, oid in enumerate(top_objs):
    start_idx = rows[oid][1]
    end_idx = rows[top_objs[i+1]][1] if i + 1 < len(top_objs) else re.search(rb"\b" + str(xref_oid).encode() + rb"\s+0\s+obj\b", pdf_bytes).start()
    obj_raw[oid] = pdf_bytes[start_idx:end_idx]

page_content_list = []
for oid in top_objs:
    raw = obj_raw[oid]
    m_s = re.search(rb"stream[\r\n]+(.*?)[\r\n]+endstream", raw, re.DOTALL)
    if m_s:
        try:
            dec = zlib.decompress(m_s.group(1))
            if b"0.07451 0.294118 0.729412 rg/R2 8 Tf" in dec:
                page_content_list.append(oid)
        except:
            pass

print("Discovered Page Content OIDs:", page_content_list)
row_pattern = re.compile(
    rb'(q\s+1\s+0\s+0\s+1\s+(?:19\.\d+|20(?:\.0+)?)\s+([\d\.]+)\s+cm\s+BT\s+0\s+0\s+0\s+rg/R1\s+8\s+Tf(/R\d+\s+gs).*?0\.07451\s+0\.294118\s+0\.729412\s+rg/R2\s+8\s+Tf.*?ET\s+Q)',
    re.DOTALL
)

for p_idx, oid in enumerate(page_content_list):
    raw = obj_raw[oid]
    m_s = re.search(rb"stream[\r\n]+(.*?)[\r\n]+endstream", raw, re.DOTALL)
    dec = zlib.decompress(m_s.group(1))
    matches = list(row_pattern.finditer(dec))
    print(f"Page {p_idx+1} (OID {oid}): found {len(matches)} row pattern matches")
