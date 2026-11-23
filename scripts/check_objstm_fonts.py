import re
import zlib

def get_base_fonts(pdf_bytes):
    fonts = set()
    for m in re.finditer(rb'stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL):
        try:
            dec = zlib.decompress(m.group(1))
            for fm in re.finditer(rb'/BaseFont\s*/([^\s>/]+)', dec):
                fonts.add(fm.group(1).decode('latin1', 'ignore'))
        except:
            pass
    return fonts

with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf", "rb") as f:
    b_k = f.read()

with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf", "rb") as f:
    b_i = f.read()

print("Keisya Sep:", get_base_fonts(b_k))
print("Ibnu Sep:", get_base_fonts(b_i))
