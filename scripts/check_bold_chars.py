import re
import zlib
import io
from fontTools.ttLib import TTFont

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

m_bold = re.search(rb'\b397\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
ttf_bold = TTFont(io.BytesIO(zlib.decompress(m_bold.group(2))))
glyf_bold = ttf_bold['glyf']

m_map_bold = re.search(rb'\b396\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
map_bold = zlib.decompress(m_map_bold.group(2))

chars = "012345 dari"
for ch in chars:
    cid = ord(ch)
    gid = (map_bold[cid*2] << 8) | map_bold[cid*2 + 1]
    gname = f"glyph{gid:05d}"
    contours = glyf_bold[gname].numberOfContours if gname in glyf_bold else -999
    print(f"Bold Char '{ch}' (CID={cid}) -> GID {gid} ({gname}): contours={contours}")
