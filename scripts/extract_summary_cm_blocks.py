import zlib
import re

ref_pdf = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf"

with open(ref_pdf, "rb") as f:
    b = f.read()

m_stream = re.search(rb'\b32\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL)
dec = zlib.decompress(m_stream.group(2))

# Find all 'q 1 0 0 1 <x> <y> cm BT ... ET Q'
blocks = list(re.finditer(rb'q\s+1\s+0\s+0\s+1\s+([\d\.]+)\s+([\d\.]+)\s+cm\s+BT.*?ET\s+Q', dec, re.DOTALL))
print("Total cm BT blocks:", len(blocks))

for b in blocks:
    x = float(b.group(1))
    y = float(b.group(2))
    # Summary box is around x in [290, 580], y in [590, 680]
    if 280 <= x <= 580 and 590 <= y <= 680:
        raw = b.group(0)
        # extract string in parens
        strings = re.findall(rb'\((.*?)\)', raw)
        decoded_strs = []
        for s in strings:
            try:
                decoded_strs.append(s.decode('utf-16-be'))
            except:
                decoded_strs.append(s.decode('latin1'))
        print(f"x={x:.2f}, y={y:.2f} -> {decoded_strs}")
        print("   raw:", raw[:120])
