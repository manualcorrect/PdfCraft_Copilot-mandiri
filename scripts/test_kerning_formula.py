import re
import zlib
import io
from fontTools.ttLib import TTFont

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# Load font widths from CIDFont 504 (Regular /R1) and 507 (Bold /R2)
# Or from TTF hmtx table!
m_reg = re.search(rb'\b394\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
ttf_reg = TTFont(io.BytesIO(zlib.decompress(m_reg.group(2))))
hmtx_reg = ttf_reg['hmtx']
units_reg = ttf_reg['head'].unitsPerEm

m_bold = re.search(rb'\b397\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
ttf_bold = TTFont(io.BytesIO(zlib.decompress(m_bold.group(2))))
hmtx_bold = ttf_bold['hmtx']
units_bold = ttf_bold['head'].unitsPerEm

# Regular CIDToGID
m_map_reg = re.search(rb'\b393\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
map_reg = zlib.decompress(m_map_reg.group(2))

# Bold CIDToGID
m_map_bold = re.search(rb'\b396\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
map_bold = zlib.decompress(m_map_bold.group(2))

def get_no_width(s):
    w = 0.0
    for ch in s:
        cid = ord(ch)
        gid = (map_reg[cid*2] << 8) | map_reg[cid*2 + 1]
        gname = f"glyph{gid:05d}"
        adv = hmtx_reg[gname][0]
        w += (adv / units_reg) * 8.0
    return w

def get_saldo_width(s):
    w = 0.0
    for ch in s:
        cid = ord(ch)
        gid = (map_bold[cid*2] << 8) | map_bold[cid*2 + 1]
        gname = f"glyph{gid:05d}"
        adv = hmtx_bold[gname][0]
        w += (adv / units_bold) * 8.0
    return w

# Test with row 59 on Page 1: No='59', Saldo='779.988,81', K=-62700
w_no = get_no_width("59")
w_sal = get_saldo_width("779.988,81")
calc_k = - round((551.00 - w_sal - w_no) / 0.008)
print(f"Row 59: w_no={w_no:.3f}, w_sal={w_sal:.3f}, actual_k=-62700, calc_k={calc_k}")

# Test with row 79 on Page 2: No='79', Saldo='2.626.488,81', K=-61815
w_no = get_no_width("79")
w_sal = get_saldo_width("2.626.488,81")
calc_k = - round((551.00 - w_sal - w_no) / 0.008)
print(f"Row 79: w_no={w_no:.3f}, w_sal={w_sal:.3f}, actual_k=-61815, calc_k={calc_k}")
