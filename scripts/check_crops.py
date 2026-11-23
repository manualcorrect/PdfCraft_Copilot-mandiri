from PIL import Image

im1 = Image.open(r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\crop_user_aug_output1.png")
im2 = Image.open(r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\crop_user_ref_mar.png")
print("crop1:", im1.size)
print("crop2:", im2.size)
