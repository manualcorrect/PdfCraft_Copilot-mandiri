import re
import zlib

with open("output/REK_IBNU_AUG_OUTPUT_1.pdf", "rb") as f:
    pdf_bytes = f.read()

m = re.search(rb'\b12\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
dec = zlib.decompress(m.group(2)).decode('latin1', errors='ignore')

pos_c1 = dec.find('446.12 667')
pos_c4 = dec.find('446.12 597')
start_b1 = dec.rfind('q', 0, pos_c1)
m_end_b1 = re.search(r'ET\s*Q', dec[pos_c4:])
end_b1 = pos_c4 + m_end_b1.end() if m_end_b1 else -1

print(f"start_b1={start_b1}, pos_c1={pos_c1}, pos_c4={pos_c4}, end_b1={end_b1}")

pos_now = dec.find('16 676 cm')
end_b2 = dec.rfind('q', 0, pos_now)
matches_b2 = list(re.finditer(r'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+667\s+cm', dec[end_b1:end_b2]))
if not matches_b2:
    matches_b2 = list(re.finditer(r'q\s+1\s+0\s+0\s+1\s+0\s+0\s+cm', dec[end_b1:end_b2]))
print(f"pos_now={pos_now}, end_b2={end_b2}, matches_b2 len={len(matches_b2)}")
if matches_b2:
    start_b2 = end_b1 + matches_b2[-1].start()
    print(f"start_b2={start_b2}")
    print("Block 2 slice:")
    print(dec[start_b2:end_b2])
