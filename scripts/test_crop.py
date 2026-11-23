from PIL import Image

im1 = Image.open(r"C:/Users/Wisnu/.gemini/antigravity/brain/5e8306ab-a513-43f6-bf81-265c0e523098/.user_uploaded/media_1794538831328_d03cb0dd.jpg")
print(im1.size)
# The whole page is displayed in PdfCraft
# Let's save a crop of y from 200 to 450, x from 500 to 900
c = im1.crop((520, 240, 880, 360))
c.save(r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\test_crop.png")
