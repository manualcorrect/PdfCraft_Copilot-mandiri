import re, zlib
from test_xref_sep import obj_raw

raw10 = obj_raw[10]
m_len = re.search(rb'/Length\s+(\d+)', raw10)
length = int(m_len.group(1))
m_stream = re.search(rb'stream(\r\n|\n)', raw10)
stream_data = raw10[m_stream.end() : m_stream.end() + length]
stext = zlib.decompress(stream_data).decode('latin1', errors='ignore')

# Check Block 1
pos_c1 = stext.find('446.12 667')
start_b1 = stext.rfind('q', 0, pos_c1)
pos_c4 = stext.find('446.12 597')
m_end_b1 = re.search(r'ET\s*Q', stext[pos_c4:])
end_b1 = pos_c4 + m_end_b1.end()

print(f"B1 start: {start_b1}, B1 end: {end_b1}")
print("B1 snippet:\n", stext[start_b1:end_b1][:200])

# Check Block 2
pos_now = stext.find('16 676 cm')
end_b2 = stext.rfind('q', 0, pos_now)
matches_b2 = list(re.finditer(r'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+667\s+cm', stext[end_b1:end_b2]))
if not matches_b2:
    matches_b2 = list(re.finditer(r'q\s+1\s+0\s+0\s+1\s+0\s+0\s+cm', stext[end_b1:end_b2]))

start_b2 = end_b1 + matches_b2[-1].start()
print(f"B2 start: {start_b2}, B2 end: {end_b2}")
print("B2 snippet:\n", stext[start_b2:end_b2][:200])
