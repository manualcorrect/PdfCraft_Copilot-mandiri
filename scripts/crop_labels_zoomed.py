import numpy as np
from PIL import Image

im1 = Image.open(r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\crop_user_aug_output1.png")
im2 = Image.open(r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\crop_user_ref_mar.png")

# Let's save a clean zoomed crop of just the 4 lines of labels and colons
# In im1 and im2, let's find the text lines
print("im1 size:", im1.size)
print("im2 size:", im2.size)

# Crop the left side (labels and colons): x from 0 to 250, y from 0 to 140
c1_labels = im1.crop((0, 0, 250, 140))
c2_labels = im2.crop((0, 0, 250, 140))

c1_labels.save(r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\labels_user_aug.png")
c2_labels.save(r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\labels_user_ref.png")
print("Saved labels_user_aug.png and labels_user_ref.png!")
