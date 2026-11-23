import zlib
import re
from fontTools.ttLib import TTFont
import io

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

m = re.search(rb'\b639\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
dec = zlib.decompress(m.group(2))
ttf = TTFont(io.BytesIO(dec))
hmtx = ttf['hmtx']
glyf = ttf['glyf']

g49 = ttf.getGlyphOrder()[49]
print("Glyph 49 name:", g49)
print("Glyph 49 advance width & lsb:", hmtx[g49])
print("Glyph 49 numberOfContours:", glyf[g49].numberOfContours)
