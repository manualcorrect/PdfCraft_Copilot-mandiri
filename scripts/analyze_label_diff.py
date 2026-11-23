import numpy as np
from PIL import Image

im_aug = Image.open(r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\labels_user_aug.png")
im_ref = Image.open(r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\labels_user_ref.png")

# Let's inspect differences
arr_aug = np.array(im_aug)
arr_ref = np.array(im_ref)

print("Aug shape:", arr_aug.shape)
print("Ref shape:", arr_ref.shape)

# Let's check diff
diff = np.abs(arr_aug.astype(float) - arr_ref.astype(float))
print("Max diff:", diff.max(), "Mean diff:", diff.mean())

# Find where diff > 30
diff_mask = diff.mean(axis=2) > 30
rows_diff = np.where(diff_mask.any(axis=1))[0]
cols_diff = np.where(diff_mask.any(axis=0))[0]

if len(rows_diff) > 0:
    print(f"Diff rows: y from {rows_diff[0]} to {rows_diff[-1]}")
    print(f"Diff cols: x from {cols_diff[0]} to {cols_diff[-1]}")
