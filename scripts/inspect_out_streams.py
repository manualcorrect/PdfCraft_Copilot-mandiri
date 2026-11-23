import re
import zlib

with open("output/REK_IBNU_AUG_OUTPUT_1.pdf", "rb") as f:
    pdf_bytes = f.read()

for m in re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL):
    oid = int(m.group(1))
    d = m.group(2)
    s = m.group(3)
    try:
        dec = zlib.decompress(s)
        has_color = b"0.07451" in dec
        # check what date strings appear
        dates_found = [m.group(0).decode() for m in re.finditer(rb'\b\d{2}\s+Aug\s+2026\b', dec)]
        print(f"Obj {oid}: stream len={len(dec)} has_color={has_color} dates_count={len(dates_found)} dates={dates_found[:3]}")
    except Exception as e:
        print(f"Obj {oid}: decompress failed {e}")
