import zlib
import re
from fontTools.ttLib import TTFont
import io

with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf", "rb") as f:
    b_aug = f.read()

with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf", "rb") as f:
    b_sep = f.read()

# August font 601
m_aug = re.search(rb'\b601\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b_aug, re.DOTALL)
ttf_aug = TTFont(io.BytesIO(zlib.decompress(m_aug.group(2))))

# September font 639
m_sep = re.search(rb'\b639\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b_sep, re.DOTALL)
ttf_sep = TTFont(io.BytesIO(zlib.decompress(m_sep.group(2))))

g_aug_c = ttf_aug.getGlyphOrder()[50]
print("Aug 'c' glyph name:", g_aug_c)
print("Aug 'c' contours:", ttf_aug['glyf'][g_aug_c].numberOfContours)
print("Aug 'c' hmtx:", ttf_aug['hmtx'][g_aug_c])

# Copy glyph into September glyph 49!
g_sep_c = ttf_sep.getGlyphOrder()[49]
ttf_sep['glyf'][g_sep_c] = ttf_aug['glyf'][g_aug_c]
ttf_sep['hmtx'][g_sep_c] = ttf_aug['hmtx'][g_aug_c]

out_buf = io.BytesIO()
ttf_sep.save(out_buf)
new_ttf_bytes = out_buf.getvalue()
print("Successfully patched TTF! New length:", len(new_ttf_bytes))

# Now test updating CIDToGIDMap 638:
m_map = re.search(rb'\b638\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b_sep, re.DOTALL)
map_bytes = bytearray(zlib.decompress(m_map.group(2)))
cid_c = ord('c') # 99
map_bytes[cid_c*2] = 0
map_bytes[cid_c*2 + 1] = 49
print(f"Patched map: CID 99 -> GID {(map_bytes[cid_c*2]<<8) | map_bytes[cid_c*2+1]}")
