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
    print("Font 639 tables:", ttf.keys())
    cmap = ttf.getBestCmap()
    print("Total cmap entries:", len(cmap) if cmap else 0)
    for code in [ord('C'), ord('i'), ord('c'), ord('e'), ord('r')]:
        ch = chr(code)
        mapped = cmap.get(code, "MISSING") if cmap else "NO CMAP"
        print(f"Char '{ch}' (code {code}): mapped to {mapped}")
