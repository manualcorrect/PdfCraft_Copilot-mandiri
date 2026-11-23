import re
import zlib
import io
import sys
from fontTools.ttLib import TTFont

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\test_step3.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# Load authentic font metrics from 0.pdf
orig_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\0.pdf"
with open(orig_pdf, "rb") as f0:
    b0 = f0.read()
    ttf_reg = TTFont(io.BytesIO(zlib.decompress(re.search(rb'\b541\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b0, re.DOTALL).group(2))))
    ttf_bold = TTFont(io.BytesIO(zlib.decompress(re.search(rb'\b544\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b0, re.DOTALL).group(2))))
    map_reg = zlib.decompress(re.search(rb'\b539\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b0, re.DOTALL).group(2))
    map_bold = zlib.decompress(re.search(rb'\b543\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b0, re.DOTALL).group(2))

hmtx_reg = ttf_reg['hmtx']
units_reg = ttf_reg['head'].unitsPerEm
hmtx_bold = ttf_bold['hmtx']
units_bold = ttf_bold['head'].unitsPerEm

def get_reg_width(s):
    w = 0.0
    for ch in s:
        cid = ord(ch)
        gid = (map_reg[cid*2] << 8) | map_reg[cid*2 + 1]
        adv = hmtx_reg[f"glyph{gid:05d}"][0]
        w += (adv / units_reg) * 8.0
    return w

def get_bold_width(s):
    w = 0.0
    for ch in s:
        cid = ord(ch)
        gid = (map_bold[cid*2] << 8) | map_bold[cid*2 + 1]
        adv = hmtx_bold[f"glyph{gid:05d}"][0]
        w += (adv / units_bold) * 8.0
    return w

def to_utf16_be(s: str) -> bytes:
    return s.encode("utf-16-be")

page_oids = [12, 114, 214, 313, 412, 512]
PAGE_RIGHT_X = 563.80

for pn, oid in enumerate(page_oids, start=1):
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    decomp = zlib.decompress(m.group(2))
    
    s_bold = f"{pn} dari 7"
    w_b = get_bold_width(s_bold)
    x_b = PAGE_RIGHT_X - w_b
    
    s_it = f"{pn} of 7"
    w_it = get_reg_width(s_it)
    x_it = PAGE_RIGHT_X - w_it
    
    page_num_replacements = []
    
    m_it = re.search(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+726\s+cm\s+BT\s+0\s+0\s+0\s+rg/R3\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', decomp, re.DOTALL)
    assert m_it is not None
    gs_it = m_it.group(1)
    new_it = (
        f"q 1 0 0 1 {x_it:.2f} 726 cm BT 0 0 0 rg/R1 8 Tf 1 0 0.2 1 0 0 Tm".encode() +
        gs_it + b"(" + to_utf16_be(s_it) + b") Tj ET Q"
    )
    page_num_replacements.append((m_it.start(), m_it.end(), new_it))
    
    bold_blocks = list(re.finditer(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+736\s+cm\s+BT\s+0\s+0\s+0\s+rg/R2\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', decomp, re.DOTALL))
    assert len(bold_blocks) >= 1
    gs_b = bold_blocks[-1].group(1)
    new_b = (
        f"q 1 0 0 1 {x_b:.2f} 736 cm BT 0 0 0 rg/R2 8 Tf".encode() +
        gs_b + b"(" + to_utf16_be(s_bold) + b") Tj ET Q"
    )
    page_num_replacements.append((bold_blocks[0].start(), bold_blocks[0].end(), new_b))
    for extra_bb in bold_blocks[1:]:
        page_num_replacements.append((extra_bb.start(), extra_bb.end(), b""))
        
    page_num_replacements.sort(key=lambda x: x[0], reverse=True)
    for start_pos, end_pos, repl_bytes in page_num_replacements:
        decomp = decomp[:start_pos] + repl_bytes + decomp[end_pos:]
        
    print(f"Page {pn} (OID {oid}) patched successfully: '{s_bold}' (x={x_b:.2f}) & '{s_it}' (x={x_it:.2f})")
