from PIL import Image

im1 = Image.open(r"C:/Users/Wisnu/.gemini/antigravity/brain/5e8306ab-a513-43f6-bf81-265c0e523098/.user_uploaded/media_1794538831328_d03cb0dd.jpg")
im2 = Image.open(r"C:/Users/Wisnu/.gemini/antigravity/brain/5e8306ab-a513-43f6-bf81-265c0e523098/.user_uploaded/media_1794538835953_fdef0fb8.jpg")

# In 1024x576 image:
# Find exact coordinates of summary box
# Let's crop x from 550 to 900, y from 260 to 380
crop1 = im1.crop((550, 260, 900, 380))
crop2 = im2.crop((550, 260, 900, 380))

crop1.save(r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\summary_box_aug.png")
crop2.save(r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\summary_box_ref.png")
print("Saved summary_box_aug.png and summary_box_ref.png")
