import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

m = re.search(rb'\b402\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
decomp = zlib.decompress(m.group(2))

# Look around 779.988,81
idx = decomp.find("779.988,81".encode("utf-16-be"))
print("Page 1 Row 1 block:")
print(decomp[idx-150:idx+60])
