import zlib
import re

ref_pdf = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf"

with open(ref_pdf, "rb") as f:
    b = f.read()

m_stream = re.search(rb'\b32\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL)
dec = zlib.decompress(m_stream.group(2))

# Let's find BT 1 0 0 1 446.12 667 Tm through the end of the summary box
pos1 = dec.find(b"BT\n1 0 0 1 446.12 667 Tm")
pos2 = dec.find(b"BT\n1 0 0 1 530.8 597 Tm")
pos2_end = dec.find(b"ET", pos2) + 2

summary_chunk = dec[pos1:pos2_end]
print("Summary chunk from ref_pdf length:", len(summary_chunk))
print(summary_chunk.decode('latin1', errors='ignore'))
