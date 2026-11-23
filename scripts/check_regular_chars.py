import re
import zlib
import io
from fontTools.ttLib import TTFont

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

m_reg = re.search(rb'\b394\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
ttf_reg = TTFont(io.BytesIO(zlib.decompress(m_reg.group(2))))
glyf = ttf_reg['glyf']

m_map_reg = re.search(rb'\b393\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
map_reg = zlib.decompress(m_map_reg.group(2))

chars = "0123456789of dari"
for ch in chars:
    cid = ord(ch)
    gid = (map_reg[cid*2] << 8) | map_reg[cid*2 + 1]
    gname = f"glyph{gid:05d}"
    contours = glyf[gname].numberOfContours if gname in glyf else -999
    print(f"Char '{ch}' (CID={cid}) -> GID {gid} ({gname}): contours={contours}")
