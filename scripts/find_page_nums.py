import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

page_objs = [402, 1, 102, 203, 304]
for p_idx, oid in enumerate(page_objs, 1):
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    decomp = zlib.decompress(m.group(2))
    print(f"\n================ Page {p_idx} (Obj {oid}) ================")
    # Find all cm BT ... ET blocks with x near 530..570 and y near 710..745
    for b in re.finditer(rb'q\s+1\s+0\s+0\s+1\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+cm\s+BT\s+(.*?)\s+ET\s+Q', decomp, re.DOTALL):
        x = float(b.group(1))
        y = float(b.group(2))
        if 520 <= x <= 570 and 715 <= y <= 745:
            content = b.group(3)
            # decode utf16 strings
            strings = re.findall(rb'\(([^\)]*)\)', content)
            text_repr = []
            for s in strings:
                try:
                    text_repr.append(s.decode('utf-16-be'))
                except:
                    text_repr.append(str(s))
            print(f"  x={x:.2f}, y={y:.2f}: {b.group(0)}")
            print(f"    Decoded: {' | '.join(text_repr)}")
