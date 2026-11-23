import zlib
import re

aug_out_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\REK_KEISYA_AUG_OUTPUT_1.pdf"

with open(aug_out_pdf, "rb") as f:
    b = f.read()

# Let's inspect Page 1 content stream (Obj 12 or whatever)
# Find obj that contains "Menara Mandiri"
for m in re.finditer(rb'(\d+)\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b, re.DOTALL):
    oid = int(m.group(1))
    try:
        dec = zlib.decompress(m.group(3))
        if b"Menara" in dec or b"\x00M\x00e\x00n\x00a\x00r\x00a" in dec:
            print(f"Page 1 stream is OID {oid}!")
            # Find all BT blocks around y in [590, 680]
            # Print lines between y=590 and y=680
            for line in dec.splitlines():
                if any(k in line for k in [b" 667 ", b" 644 ", b" 621 ", b" 597 ", b" 643.", b" 620.", b" 597."]):
                    print("  Line:", line[:120])
                if b"002D" in line or b"002B" in line or b"00310030" in line:
                    print("  HexLine:", line[:120])
    except:
        pass
