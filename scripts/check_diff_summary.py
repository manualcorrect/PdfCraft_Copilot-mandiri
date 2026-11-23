from PIL import Image, ImageChops
import os

out_dir = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098"
im1 = Image.open(os.path.join(out_dir, "highres_orig_summary.png"))
im2 = Image.open(os.path.join(out_dir, "highres_out_summary.png"))

diff = ImageChops.difference(im1, im2)
diff.save(os.path.join(out_dir, "diff_summary.png"))

# Let's crop each of the 4 rows:
# Row 1: Saldo Awal
# Row 2: Dana Masuk
# Row 3: Dana Keluar
# Row 4: Saldo Akhir

# Height of summary box in highres (scale 3): 780 - 450 = 330 px
# Let's crop Row 3 (Dana Keluar): y from ~180 to ~250
r3_orig = im1.crop((0, 170, im1.width, 260))
r3_out = im2.crop((0, 170, im2.width, 260))

r3_orig.save(os.path.join(out_dir, "r3_orig_danakeluar.png"))
r3_out.save(os.path.join(out_dir, "r3_out_danakeluar.png"))

print("Saved difference and row 3 crops!")
