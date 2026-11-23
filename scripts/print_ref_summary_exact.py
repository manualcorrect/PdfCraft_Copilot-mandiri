import zlib
import re

ref_pdf = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf"

with open(ref_pdf, "rb") as f:
    b = f.read()

m_stream = re.search(rb'\b32\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL)
dec = zlib.decompress(m_stream.group(2))

# Let's find all occurrences of 298, 446.12, 567 in the stream
lines = dec.split(b'ET')
for l in lines:
    if any(k in l for k in [b'298', b'446.12', b'505.96', b'508.32', b'521.32', b'530.8']):
        print(b'ET' + l + b'\n------------------------')
