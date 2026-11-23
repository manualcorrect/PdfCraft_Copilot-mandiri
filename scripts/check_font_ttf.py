import zlib
import re
from fontTools.ttLib import TTFont
import io

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# Let's find font file for RMHACJ
for m in re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL):
    oid = int(m.group(1))
    d = m.group(2)
    s = m.group(3)
    if b"/FontFile2" in d or len(s) > 3000:
        try:
            dec = zlib.decompress(s)
            if dec[:4] in [b'\x00\x01\x00\x00', b'true', b'typ1', b'OTTO']:
                ttf = TTFont(io.BytesIO(dec))
                name = ttf['name'].getDebugName(6)
                print(f"Obj {oid} is font: {name}")
                if 'Regular' in name or 'Interphases-' in name:
                    # check glyphs
                    glyph_names = ttf.getGlyphOrder()
                    print(f"  Total glyphs: {len(glyph_names)}")
                    has_c = 'c' in glyph_names or 'glyph00067' in glyph_names
                    print(f"  Has 'c' in glyphOrder? {'c' in glyph_names}")
                    # check cmap
                    cmap = ttf.getBestCmap()
                    print(f"  ord('c') (99) in cmap? {99 in cmap if cmap else 'No cmap'}")
                    if cmap and 99 in cmap:
                        print(f"  mapped glyph for 99: {cmap[99]}")
        except:
            pass
