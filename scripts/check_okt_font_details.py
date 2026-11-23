import re
import zlib
import io
import sys
from fontTools.ttLib import TTFont

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

def get_stream(oid):
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    return zlib.decompress(m.group(2))

ttf_reg = TTFont(io.BytesIO(get_stream(541)))
map_reg = get_stream(539)

ttf_bold = TTFont(io.BytesIO(get_stream(544)))
map_bold = get_stream(543)

ttf_it = TTFont(io.BytesIO(get_stream(547)))
map_it = get_stream(546)

print("--- REGULAR (541 with map 539) ---")
glyf_reg = ttf_reg['glyf']
for ch in "0123456789 .,:()-+/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
    cid = ord(ch)
    gid = (map_reg[cid*2] << 8) | map_reg[cid*2 + 1]
    gname = f"glyph{gid:05d}"
    contours = glyf_reg[gname].numberOfContours if gname in glyf_reg else -999
    if contours <= 0 and ch != ' ':
        print(f"Missing in Regular: '{ch}' (CID={cid}) -> GID {gid} ({gname}) contours={contours}")

print("\n--- BOLD (544 with map 543) ---")
glyf_bold = ttf_bold['glyf']
for ch in "0123456789 dari":
    cid = ord(ch)
    gid = (map_bold[cid*2] << 8) | map_bold[cid*2 + 1]
    gname = f"glyph{gid:05d}"
    contours = glyf_bold[gname].numberOfContours if gname in glyf_bold else -999
    print(f"Bold '{ch}': GID {gid} contours={contours}")

print("\n--- ITALIC (547 with map 546) ---")
glyf_it = ttf_it['glyf']
for ch in "0123456789 of":
    cid = ord(ch)
    gid = (map_it[cid*2] << 8) | map_it[cid*2 + 1]
    gname = f"glyph{gid:05d}"
    contours = glyf_it[gname].numberOfContours if gname in glyf_it else -999
    print(f"Italic '{ch}': GID {gid} contours={contours}")
