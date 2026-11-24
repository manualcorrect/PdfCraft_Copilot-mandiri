import re, zlib
from test_xref_sep import obj_raw

oids = [10, 113, 212, 311]
for p_num, oid in enumerate(oids, 1):
    raw = obj_raw[oid]
    m_len = re.search(rb'/Length\s+(\d+)', raw)
    length = int(m_len.group(1))
    m_stream = re.search(rb'stream(\r\n|\n)', raw)
    stream_data = raw[m_stream.end() : m_stream.end() + length]
    dec = zlib.decompress(stream_data)
    
    # Check italic block (at y=726)
    m_it = re.search(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+726\s+cm\s+BT\s+0\s+0\s+0\s+rg/R3\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', dec, re.DOTALL)
    # Check bold block (at y=736)
    bold_blocks = list(re.finditer(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+736\s+cm\s+BT\s+0\s+0\s+0\s+rg/R2\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', dec, re.DOTALL))
    
    print(f"Page {p_num} (OID {oid}): italic block found = {m_it is not None}, bold blocks count = {len(bold_blocks)}")
