import re
import zlib
import pypdfium2 as pdfium
import pdfplumber
import io

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = bytearray(f.read())

m = re.search(rb'\b402\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
decomp = zlib.decompress(m.group(2))

old_it = b'q 1 0 0 1 542.4 726 cm BT 0 0 0 rg/R3 8 Tf/R34 gs(\x001\x00 ) Tj(\x00o\x00f\x00 \x001) Tj[ 2(\x000)]TJ ET Q'
new_it = b'q 1 0 0 1 545.71 726 cm BT 0 0 0 rg/R1 8 Tf 1 0 0.2 1 0 0 Tm/R34 gs(\x001\x00 \x00o\x00f\x00 \x005) Tj ET Q'

old_b10 = b'q 1 0 0 1 555.84 736 cm BT 0 0 0 rg/R2 8 Tf/R37 gs(\x001\x000) Tj ET Q'
old_b1 = b'q 1 0 0 1 534.28 736 cm BT 0 0 0 rg/R2 8 Tf/R38 gs(\x001\x00 \x00d\x00a\x00r\x00i) Tj ET Q'
new_b = b'q 1 0 0 1 537.41 736 cm BT 0 0 0 rg/R2 8 Tf/R38 gs(\x001\x00 \x00d\x00a\x00r\x00i\x00 \x005) Tj ET Q'

decomp = decomp.replace(old_it, new_it, 1)
decomp = decomp.replace(old_b10, b'', 1)
decomp = decomp.replace(old_b1, new_b, 1)

new_comp = zlib.compress(decomp, 9)

before_stream = pdf_bytes[:m.start(2)]
before_stream = re.sub(rb'/Length\s+\d+', f'/Length {len(new_comp)}'.encode(), before_stream)
after_stream = pdf_bytes[m.end(2):]

test_pdf = before_stream + new_comp + after_stream
with pdfplumber.open(io.BytesIO(test_pdf)) as pdf:
    words = [w for w in pdf.pages[0].extract_words() if w['top'] < 130 and w['x0'] > 500]
    for w in words:
        print(f"{w['text']} at top={w['top']:.2f}, x0={w['x0']:.2f}, x1={w['x1']:.2f}")
