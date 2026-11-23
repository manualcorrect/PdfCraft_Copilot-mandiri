import zlib, re

with open('output/REK_IBNU_OKT_OUTPUT_1.pdf', 'rb') as f:
    pdf_bytes = f.read()

m = re.search(rb'\b12\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
stext = zlib.decompress(m.group(2)).decode('latin1', errors='ignore')

pos_c1 = stext.find('446.12 667')
start_b1 = stext.rfind('q', 0, pos_c1)
pos_c4 = stext.find('446.12 597')
m_end_b1 = re.search(r'ET\s*Q', stext[pos_c4:])
end_b1 = pos_c4 + m_end_b1.end() if m_end_b1 else -1

pos_now = stext.find('16 676 cm')
end_b2 = stext.rfind('q', 0, pos_now)
matches_b2 = list(re.finditer(r'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+667\s+cm', stext[end_b1:end_b2]))
if not matches_b2:
    matches_b2 = list(re.finditer(r'q\s+1\s+0\s+0\s+1\s+0\s+0\s+cm', stext[end_b1:end_b2]))
start_b2 = end_b1 + matches_b2[-1].start() if matches_b2 else -1

print(f"pos_c1: {pos_c1}, start_b1: {start_b1}")
print(f"pos_c4: {pos_c4}, end_b1: {end_b1}")
print(f"pos_now: {pos_now}, end_b2: {end_b2}")
print(f"start_b2: {start_b2}")

if start_b1 != -1 and end_b1 != -1 and start_b2 != -1 and end_b2 != -1:
    print("Block 1 length:", end_b1 - start_b1)
    print("Block 1 sample:\n", stext[start_b1:start_b1+200])
    print("Block 2 length:", end_b2 - start_b2)
    print("Block 2 sample:\n", stext[start_b2:start_b2+200])
