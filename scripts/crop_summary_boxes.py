import os
from PIL import Image

img1_path = r"C:/Users/Wisnu/.gemini/antigravity/brain/5e8306ab-a513-43f6-bf81-265c0e523098/.user_uploaded/media_1794538831328_d03cb0dd.jpg"
img2_path = r"C:/Users/Wisnu/.gemini/antigravity/brain/5e8306ab-a513-43f6-bf81-265c0e523098/.user_uploaded/media_1794538835953_fdef0fb8.jpg"

im1 = Image.open(img1_path)
im2 = Image.open(img2_path)

print("Im1 size:", im1.size)
print("Im2 size:", im2.size)

# Crop summary box from both
# In 1024x576 or 1920x1080? Let's check size
# Assuming ~1024x576, the summary box is on the right side of the document
# Document is in center: ~250 to 900 x, summary box is around x=500..880, y=250..380
w, h = im1.size
box = (int(w * 0.45), int(h * 0.4), int(w * 0.9), int(h * 0.65))

c1 = im1.crop(box)
c2 = im2.crop(box)

out_dir = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098"
c1.save(os.path.join(out_dir, "crop_user_aug_output1.png"))
c2.save(os.path.join(out_dir, "crop_user_ref_mar.png"))
print("Saved comparison crops!")
