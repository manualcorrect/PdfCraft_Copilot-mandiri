import zlib, re

with open('output/REK_IBNU_OKT_OUTPUT_1.pdf', 'rb') as f:
    pdf_bytes = f.read()

# Row pattern matching x ~ 20.x
row_pattern = re.compile(
    rb'(q\s+1\s+0\s+0\s+1\s+([\d\.]+)\s+([\d\.]+)\s+cm\s+BT\s+0\s+0\s+0\s+rg/R1\s+8\s+Tf(/R\d+\s+gs).*?0\.07451\s+0\.294118\s+0\.729412\s+rg/R2\s+8\s+Tf.*?ET\s+Q)',
    re.DOTALL
)

page_oids = [12, 115, 214, 314, 413, 513]
for p_idx, oid in enumerate(page_oids):
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    dec = zlib.decompress(m.group(2))
    matches = [mat for mat in row_pattern.finditer(dec) if 19 <= float(mat.group(2)) <= 22]
    print(f"Page {p_idx+1} (OID {oid}): matched {len(matches)} row blocks")
    for mat in matches[:2]:
        print(f"  x={mat.group(2).decode()} y={mat.group(3).decode()}: {mat.group(1)[:70]}")
