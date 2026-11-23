import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

m = re.search(rb'\b402\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
decomp = zlib.decompress(m.group(2))

# Find 600.988,81 and 500.988,81
for s in [b"600.988,81", b"500.988,81", b"498.488,81"]:
    u = s.decode().encode("utf-16-be")
    idx = decomp.find(u)
    print(f"Match for {s}: idx={idx}")
    if idx != -1:
        print("  Context:", decomp[idx-80:idx+60])
