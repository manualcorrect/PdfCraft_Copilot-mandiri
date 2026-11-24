import re, zlib
from test_xref_sep import obj_raw

raw113 = obj_raw[113]
m_len = re.search(rb'/Length\s+(\d+)', raw113)
length = int(m_len.group(1))

# Find 'stream\r\n' or 'stream\n'
m_stream = re.search(rb'stream(\r\n|\n)', raw113)
stream_start = m_stream.end()
stream_data = raw113[stream_start : stream_start + length]

print(f"Declared Length: {length}, Extracted len: {len(stream_data)}")
dec = zlib.decompress(stream_data)
print(f"SUCCESS! Decompressed len: {len(dec)}")
print(f"Has table: {b'0.07451 0.294118 0.729412 rg/R2 8 Tf' in dec}")
