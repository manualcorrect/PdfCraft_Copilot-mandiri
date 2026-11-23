import re
import zlib
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\test_step3.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

page_oids = [12, 114, 214, 313, 412, 512]

row_pattern = re.compile(
    rb'(q\s+1\s+0\s+0\s+1\s+(?:19\.\d+|20(?:\.0+)?)\s+([\d\.]+)\s+cm\s+BT\s+0\s+0\s+0\s+rg/R1\s+8\s+Tf(/R\d+\s+gs)(.*?)(0\.07451\s+0\.294118\s+0\.729412\s+rg/R2\s+8\s+Tf\s*\[\s*-?\d+\s*\(([^\)]*?)\)\s*\]TJ)\s+ET\s+Q)',
    re.DOTALL
)

def get_decomp(oid):
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    return zlib.decompress(m.group(2))

for p_num, oid in enumerate(page_oids, start=1):
    decomp = get_decomp(oid)
    matches = list(row_pattern.finditer(decomp))
    print(f"Page {p_num} (OID {oid}): {len(matches)} row pattern matches")
    
    # Check page numbers
    m_it = re.search(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+726\s+cm\s+BT\s+0\s+0\s+0\s+rg/R3\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', decomp, re.DOTALL)
    print(f"  Italic block (y=726): {'FOUND' if m_it else 'NOT FOUND'}")
    if m_it:
        print(f"    Content: {m_it.group(0)[:80]}")
        
    bold_blocks = list(re.finditer(rb'q\s+1\s+0\s+0\s+1\s+[\d\.]+\s+736\s+cm\s+BT\s+0\s+0\s+0\s+rg/R2\s+8\s+Tf(/R\d+\s+gs).*?ET\s+Q', decomp, re.DOTALL))
    print(f"  Bold blocks (y=736): {len(bold_blocks)} found")
    for b in bold_blocks:
        print(f"    Content: {b.group(0)[:80]}")
