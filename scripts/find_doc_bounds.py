import os
from PIL import Image
import numpy as np

im1 = Image.open(r"C:/Users/Wisnu/.gemini/antigravity/brain/5e8306ab-a513-43f6-bf81-265c0e523098/.user_uploaded/media_1794538831328_d03cb0dd.jpg")
im2 = Image.open(r"C:/Users/Wisnu/.gemini/antigravity/brain/5e8306ab-a513-43f6-bf81-265c0e523098/.user_uploaded/media_1794538835953_fdef0fb8.jpg")

arr1 = np.array(im1)
# Mandiri blue is around R < 50, G in 100..180, B > 200
blue_mask = (arr1[:, :, 0] < 50) & (arr1[:, :, 1] > 100) & (arr1[:, :, 1] < 180) & (arr1[:, :, 2] > 200)
rows = np.where(blue_mask.any(axis=1))[0]
cols = np.where(blue_mask.any(axis=0))[0]

print("Blue banner: y from", rows[0], "to", rows[-1], "| x from", cols[0], "to", cols[-1])
# In Mandiri PDF, the blue banner is at the very top: y = 0 to ~80 pt, full width of document (x = 0 to 595 pt)
doc_x0 = cols[0]
doc_x1 = cols[-1]
doc_w = doc_x1 - doc_x0
banner_h = rows[-1] - rows[0]
# Total doc height is doc_w * (842 / 595)
doc_h = int(doc_w * 842.0 / 595.0)
doc_y0 = rows[0]
doc_y1 = doc_y0 + doc_h

print(f"Doc bounding box: x={doc_x0}..{doc_x1} (w={doc_w}), y={doc_y0}..{doc_y1} (h={doc_h})")

# Summary box in PDF:
# x: 295..575 pt -> (x/595)
# y: 165..250 pt -> (y/842)
sb_x0 = int(doc_x0 + (290 / 595.0) * doc_w)
sb_x1 = int(doc_x0 + (580 / 595.0) * doc_w)
sb_y0 = int(doc_y0 + (155 / 842.0) * doc_h)
sb_y1 = int(doc_y0 + (255 / 842.0) * doc_h)

print(f"Summary box crop: x={sb_x0}..{sb_x1}, y={sb_y0}..{sb_y1}")

c1 = im1.crop((sb_x0, sb_y0, sb_x1, sb_y1))
c2 = im2.crop((sb_x0, sb_y0, sb_x1, sb_y1))

out_dir = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098"
c1.save(os.path.join(out_dir, "exact_user_aug_sb.png"))
c2.save(os.path.join(out_dir, "exact_user_ref_sb.png"))
print("Saved exact crops successfully!")
