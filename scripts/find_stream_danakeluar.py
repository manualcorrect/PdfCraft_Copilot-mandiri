import re
import zlib
import pypdfium2 as pdfium

ref_pdf = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf"
aug_out_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\REK_KEISYA_AUG_OUTPUT_1.pdf"

with open(ref_pdf, "rb") as f:
    b_ref = f.read()

with open(aug_out_pdf, "rb") as f:
    b_out = f.read()

print("--- Searching for 'Dana' or 'Keluar' in ref_pdf streams ---")
# Find all streams in ref_pdf
for m in re.finditer(rb'stream[\r\n]+(.*?)[\r\n]+endstream', b_ref, re.DOTALL):
    try:
        dec = zlib.decompress(m.group(1))
        if b"Keluar" in dec or b"\x00K\x00e\x00l\x00u\x00a\x00r" in dec:
            print("Found in ref_pdf stream (len", len(dec), "):")
            for line in dec.splitlines():
                if b"Keluar" in line or b"\x00K\x00e\x00l\x00u\x00a\x00r" in line or b"18.273" in line or b"\x001\x008\x00.\x002" in line:
                    print("  ", line)
    except:
        pass

print("\n--- Searching for 'Dana' or 'Keluar' in aug_out_pdf streams ---")
for m in re.finditer(rb'stream[\r\n]+(.*?)[\r\n]+endstream', b_out, re.DOTALL):
    try:
        dec = zlib.decompress(m.group(1))
        if b"Keluar" in dec or b"\x00K\x00e\x00l\x00u\x00a\x00r" in dec:
            print("Found in aug_out_pdf stream (len", len(dec), "):")
            for line in dec.splitlines():
                if b"Keluar" in line or b"\x00K\x00e\x00l\x00u\x00a\x00r" in line or b"10.749" in line or b"\x001\x000\x00.\x007" in line:
                    print("  ", line)
    except:
        pass
