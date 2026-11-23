import re
import zlib

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# Let's find DescendantFonts of RMHACJ
m = re.search(rb'/BaseFont\s*/RMHACJ\+PDF-TTInterphases-[^>]*>>', pdf_bytes)
if not m:
    # search in decompressed streams
    for sm in re.finditer(rb'stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL):
        try:
            dec = zlib.decompress(sm.group(1))
            if b"RMHACJ" in dec:
                print("Found RMHACJ in stream:")
                for line in dec.splitlines():
                    if b"RMHACJ" in line or b"CIDToGIDMap" in line:
                        print(" ", line[:100])
        except:
            pass
