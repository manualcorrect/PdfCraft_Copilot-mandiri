import zlib, re

with open('output/REK_IBNU_OKT_OUTPUT_1.pdf', 'rb') as f:
    pdf_bytes = f.read()

# Let's inspect OID 12
m = re.search(rb'\b12\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
if m:
    dec = zlib.decompress(m.group(2))
    stext = dec.decode('latin1', errors='ignore')
    # search for 0.07451 or 20.010 or 83
    for line in stext.splitlines():
        if any(term in line for term in ['0.07451', '20.010', '83', '84', '20.258']):
            print(line)
