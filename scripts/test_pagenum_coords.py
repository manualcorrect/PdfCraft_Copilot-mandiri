import re
import zlib
import io
from fontTools.ttLib import TTFont

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# Load font widths
m_reg = re.search(rb'\b394\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
ttf_reg = TTFont(io.BytesIO(zlib.decompress(m_reg.group(2))))
hmtx_reg = ttf_reg['hmtx']
units_reg = ttf_reg['head'].unitsPerEm

m_bold = re.search(rb'\b397\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
ttf_bold = TTFont(io.BytesIO(zlib.decompress(m_bold.group(2))))
hmtx_bold = ttf_bold['hmtx']
units_bold = ttf_bold['head'].unitsPerEm

# CIDToGID
map_reg = zlib.decompress(re.search(rb'\b393\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL).group(2))
map_bold = zlib.decompress(re.search(rb'\b396\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL).group(2))

def get_bold_width(s):
    w = 0.0
    for ch in s:
        cid = ord(ch)
        gid = (map_bold[cid*2] << 8) | map_bold[cid*2 + 1]
        gname = f"glyph{gid:05d}"
        adv = hmtx_bold[gname][0]
        w += (adv / units_bold) * 8.0
    return w

def get_reg_width(s):
    w = 0.0
    for ch in s:
        cid = ord(ch)
        gid = (map_reg[cid*2] << 8) | map_reg[cid*2 + 1]
        gname = f"glyph{gid:05d}"
        adv = hmtx_reg[gname][0]
        w += (adv / units_reg) * 8.0
    return w

PAGE_RIGHT_X = 563.80

for p in range(1, 6):
    s_bold = f"{p} dari 5"
    w_b = get_bold_width(s_bold)
    x_b = PAGE_RIGHT_X - w_b
    
    s_it = f"{p} of 5"
    w_it = get_reg_width(s_it)
    x_it = PAGE_RIGHT_X - w_it
    print(f"Page {p}: Bold '{s_bold}' w={w_b:.2f} x0={x_b:.2f} | Italic '{s_it}' w={w_it:.2f} x0={x_it:.2f}")
