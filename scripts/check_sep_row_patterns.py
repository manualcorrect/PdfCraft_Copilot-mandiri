import re, zlib
from test_xref_sep import obj_raw

oids = [10, 113, 212, 311]
row_pattern = re.compile(
    rb'(q\s+1\s+0\s+0\s+1\s+(?:19\.\d+|20(?:\.0+)?)\s+([\d\.]+)\s+cm\s+BT\s+0\s+0\s+0\s+rg/R1\s+8\s+Tf(/R\d+\s+gs).*?0\.07451\s+0\.294118\s+0\.729412\s+rg/R2\s+8\s+Tf.*?ET\s+Q)',
    re.DOTALL
)

for p_num, oid in enumerate(oids, 1):
    raw = obj_raw[oid]
    m_len = re.search(rb'/Length\s+(\d+)', raw)
    length = int(m_len.group(1))
    m_stream = re.search(rb'stream(\r\n|\n)', raw)
    stream_data = raw[m_stream.end() : m_stream.end() + length]
    dec = zlib.decompress(stream_data)
    matches = list(row_pattern.finditer(dec))
    print(f"Page {p_num} (OID {oid}): matches = {len(matches)}")
