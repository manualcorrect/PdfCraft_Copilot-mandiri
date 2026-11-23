import zlib, re

with open('output/REK_IBNU_SEP_OUTPUT_1.pdf', 'rb') as f:
    pdf_bytes = f.read()

m = re.search(rb'\b13\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
if m:
    dec = zlib.decompress(m.group(2))
    stext = dec.decode('latin1', errors='ignore')
    print(stext[2500:5000])
