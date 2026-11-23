from PIL import Image, ImageDraw

brain_dir = r'C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098'

img_ref = Image.open(f"{brain_dir}/guideline_ref.png")
img_old = Image.open(f"{brain_dir}/guideline_old_aug.png")
img_new = Image.open(f"{brain_dir}/guideline_new_aug.png")

w, h = img_ref.size
comp = Image.new('RGB', (w * 3, h + 60), (255, 255, 255))
draw = ImageDraw.Draw(comp)

comp.paste(img_ref, (0, 60))
comp.paste(img_old, (w, 60))
comp.paste(img_new, (w * 2, 60))

draw.text((20, 20), "OFFICIAL MANDIRI REF (Baseline aligned)", fill=(0, 0, 0))
draw.text((w + 20, 20), "OLD AUG OUTPUT 1 (Dana Keluar drooping below line)", fill=(200, 0, 0))
draw.text((w * 2 + 20, 20), "NEW AUG OUTPUT 1 (100% PERFECTLY ALIGNED)", fill=(0, 150, 0))

comp.save(f"{brain_dir}/guideline_comparison_composite.png")
print("Saved guideline comparison composite!")
