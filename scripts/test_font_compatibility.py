import pdfplumber
import zlib
import re

with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf", "rb") as f:
    b_aug = f.read()

with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf", "rb") as f:
    b_sep = f.read()

map_aug = zlib.decompress(re.search(rb'\b600\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b_aug, re.DOTALL).group(2))

# Extract all chars in September 0.pdf that use RMHACJ
sep_chars = set()
with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf") as pdf:
    for page in pdf.pages:
        for c in page.chars:
            if 'RMHACJ' in c.get('fontname', ''):
                sep_chars.add(c['text'])

print(f"Total unique characters in September 0.pdf using RMHACJ: {len(sep_chars)}")
missing_in_aug = []
for ch in sorted(sep_chars):
    cid = ord(ch)
    gid = (map_aug[cid*2] << 8) | map_aug[cid*2 + 1]
    if gid == 0:
        missing_in_aug.append((ch, cid))

print(f"Characters in September RMHACJ that are missing in August map: {missing_in_aug}")
