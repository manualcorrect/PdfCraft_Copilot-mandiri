import zlib
import re

aug_out_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\REK_KEISYA_AUG_OUTPUT_1.pdf"

with open(aug_out_pdf, "rb") as f:
    b = f.read()

m = re.search(rb'\b11\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL)
dec = zlib.decompress(m.group(2))

# Find all /R... font invocations in Obj 11
fonts_used = set(re.findall(rb'/(R\d+)\s+[\d\.]+\s+Tf', dec))
print("Fonts used in Obj 11:", fonts_used)

# Find where fonts are used
for fn in sorted(fonts_used):
    samples = []
    for m_f in re.finditer(rb'/' + fn + rb'\s+[\d\.]+\s+Tf.*?(?:Tj|TJ)', dec):
        samples.append(m_f.group(0)[:60])
        if len(samples) >= 3: break
    print(f"\nFont /{fn.decode()}:")
    for s in samples:
        print("   ", s)
