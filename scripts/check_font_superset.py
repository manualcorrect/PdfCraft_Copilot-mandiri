import re
import zlib

with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf", "rb") as f:
    b_aug = f.read()

with open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\sep\0.pdf", "rb") as f:
    b_sep = f.read()

map_aug = zlib.decompress(re.search(rb'\b600\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b_aug, re.DOTALL).group(2))
map_sep = zlib.decompress(re.search(rb'\b638\s+0\s+obj\s*<<(.*?)>>\s*stream[\r\n]+(.*?)[\r\n]+endstream', b_sep, re.DOTALL).group(2))

mismatch = []
for cid in range(128):
    gid_aug = (map_aug[cid*2] << 8) | map_aug[cid*2 + 1]
    gid_sep = (map_sep[cid*2] << 8) | map_sep[cid*2 + 1]
    if gid_sep != 0 and gid_sep != gid_aug:
        mismatch.append((cid, chr(cid), gid_aug, gid_sep))

print("Mismatches between August and September Regular maps:", mismatch)
