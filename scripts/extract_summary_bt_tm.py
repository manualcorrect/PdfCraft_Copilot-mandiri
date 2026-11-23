import zlib
import re

ref_pdf = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf"

with open(ref_pdf, "rb") as f:
    b = f.read()

m_stream = re.search(rb'\b32\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL)
dec = zlib.decompress(m_stream.group(2))

# Find all BT ... ET
bts = list(re.finditer(rb'BT(.*?)ET', dec, re.DOTALL))
print("Total BT blocks:", len(bts))

for i, bt in enumerate(bts):
    raw = bt.group(0)
    # Check if any Tm or Td in range y in [590, 680]
    m_tm = re.search(rb'1\s+0\s+0\s+1\s+([\d\.]+)\s+([\d\.]+)\s+Tm', raw)
    m_td = re.search(rb'([\d\.]+)\s+([\d\.]+)\s+Td', raw)
    
    x, y = None, None
    if m_tm:
        x, y = float(m_tm.group(1)), float(m_tm.group(2))
    elif m_td:
        x, y = float(m_td.group(1)), float(m_td.group(2))
        
    if x is not None and 280 <= x <= 580 and 590 <= y <= 680:
        strings = re.findall(rb'\((.*?)\)', raw)
        decoded_strs = []
        for s in strings:
            try:
                decoded_strs.append(s.decode('utf-16-be'))
            except:
                decoded_strs.append(s.decode('latin1'))
        print(f"BT #{i+1} at x={x:.2f}, y={y:.2f} -> {decoded_strs}")
        print("   raw:", raw.replace(b'\n', b' ')[:120])
