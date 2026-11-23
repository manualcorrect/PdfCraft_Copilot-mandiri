import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

m = re.search(rb'\b402\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
decomp = zlib.decompress(m.group(2))

# Split decomp into q ... Q blocks
blocks = re.findall(rb'q\s+1\s+0\s+0\s+1\s+([\d\.]+)\s+([\d\.]+)\s+cm\s+BT\s+(.*?)\s+ET\s+Q', decomp, re.DOTALL)
print(f"Total q cm BT blocks in Page 1: {len(blocks)}")
# Print blocks with y between 70 and 500
for x, y, content in blocks:
    fx, fy = float(x), float(y)
    if 70 <= fy <= 500:
        # extract utf16 text
        strings = re.findall(rb'\(([^\)]*)\)', content)
        text_repr = []
        for s in strings:
            try:
                text_repr.append(s.decode('utf-16-be'))
            except:
                pass
        t_str = " ".join(text_repr).strip()
        if t_str:
            print(f"  x={fx:>6.2f}, y={fy:>6.2f}: {t_str[:40]}")
