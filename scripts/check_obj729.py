import zlib, re

with open('output/REK_IBNU_SEP_OUTPUT_1.pdf', 'rb') as f:
    pdf_bytes = f.read()

m = re.search(rb'\b752\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
dict_part = m.group(1).decode('latin1')
stream_part = m.group(2)
dec = zlib.decompress(stream_part)

m_n = re.search(r'/N\s+(\d+)', dict_part)
m_first = re.search(r'/First\s+(\d+)', dict_part)
n = int(m_n.group(1))
first = int(m_first.group(1))

header_text = dec[:first].decode('latin1')
nums = [int(x) for x in header_text.split()]
pairs = [(nums[i*2], nums[i*2+1]) for i in range(n)]

print("Total pairs:", len(pairs))
for idx, (oid, off) in enumerate(pairs):
    print(f"Index {idx}: oid={oid}, offset={off}")
