import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

page_objs = {1: 402, 2: 1, 3: 102, 4: 203, 5: 304}
expected_counts = {1: 10, 2: 12, 3: 12, 4: 12, 5: 4}

row_pattern = re.compile(
    rb'(q\s+1\s+0\s+0\s+1\s+(?:19\.\d+|20(?:\.0+)?)\s+([\d\.]+)\s+cm\s+BT\s+0\s+0\s+0\s+rg/R1\s+8\s+Tf(/R\d+\s+gs)(.*?)(0\.07451\s+0\.294118\s+0\.729412\s+rg/R2\s+8\s+Tf\s*\[\s*-?\d+\s*\(([^\)]*?)\)\s*\]TJ)\s+ET\s+Q)',
    re.DOTALL
)

total_matched = 0
for p_num, oid in page_objs.items():
    m = re.search(rb'\b' + str(oid).encode() + rb'\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
    decomp = zlib.decompress(m.group(2))
    matches = list(row_pattern.finditer(decomp))
    print(f"Page {p_num} (Obj {oid}): found {len(matches)} rows (expected {expected_counts[p_num]})")
    total_matched += len(matches)
    for i, match in enumerate(matches):
        y = match.group(2).decode()
        old_sal = match.group(6).decode('utf-16-be', 'ignore')
        print(f"  Row {i+1:2d}: y={y:>7}, Saldo={old_sal}")

print(f"\nTotal matched rows: {total_matched} / 50")
