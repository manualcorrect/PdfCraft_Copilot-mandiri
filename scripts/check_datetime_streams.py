import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

m = re.search(rb'\b402\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
decomp = zlib.decompress(m.group(2))

# Find WIB
matches = list(re.finditer(rb'(\([^\)]*?\x00W\x00I\x00B[^\)]*?\))\s*Tj', decomp))
print(f"Page 1: found {len(matches)} WIB matches")
for match in matches[:3]:
    start = max(0, match.start() - 100)
    end = min(len(decomp), match.end() + 50)
    print("Match context:", decomp[start:end])
