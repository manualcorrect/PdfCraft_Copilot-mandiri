import zlib
import re
from fontTools.ttLib import TTFont
import io

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

m = re.search(rb'\b639\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
if m:
    dec = zlib.decompress(m.group(2))
    ttf = TTFont(io.BytesIO(dec))
    glyphs = ttf.getGlyphOrder()
    print("Total glyphs in font 639:", len(glyphs))
    print("Glyph names:", glyphs[:30])
    for g in glyphs:
        if 'c' in g.lower():
            print("  matching glyph:", g)
