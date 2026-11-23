import pdfplumber
from PIL import Image

ref_p = r'C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf'
old_p = 'output/REK_KEISYA_AUG_OUTPUT_1.pdf'
new_p = 'output/test_aug_perfect_sb.pdf'

# Crop box in points: (x0=280, top=160, x1=580, bottom=260)
crop_box = (280, 160, 580, 260)

def render_crop(pdf_path, out_img):
    with pdfplumber.open(pdf_path) as pdf:
        p0 = pdf.pages[0]
        # render at 300 dpi (resolution=300)
        im = p0.crop(crop_box).to_image(resolution=300)
        im.save(out_img)
        print(f"Saved {out_img}")

brain_dir = r'C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098'
render_crop(ref_p, f"{brain_dir}/sb_crop_ref.png")
render_crop(old_p, f"{brain_dir}/sb_crop_old_aug.png")
render_crop(new_p, f"{brain_dir}/sb_crop_new_aug.png")

# Also create side-by-side composite
img_ref = Image.open(f"{brain_dir}/sb_crop_ref.png")
img_old = Image.open(f"{brain_dir}/sb_crop_old_aug.png")
img_new = Image.open(f"{brain_dir}/sb_crop_new_aug.png")

w, h = img_ref.size
comp = Image.new('RGB', (w * 3, h + 60), (255, 255, 255))
from PIL import ImageDraw, ImageFont
draw = ImageDraw.Draw(comp)

comp.paste(img_ref, (0, 60))
comp.paste(img_old, (w, 60))
comp.paste(img_new, (w * 2, 60))

draw.text((20, 20), "OFFICIAL MANDIRI REF", fill=(0, 0, 0))
draw.text((w + 20, 20), "OLD AUG OUTPUT 1 (Drooping)", fill=(200, 0, 0))
draw.text((w * 2 + 20, 20), "NEW AUG OUTPUT 1 (PERFECT)", fill=(0, 150, 0))

comp.save(f"{brain_dir}/sb_comparison_composite.png")
print("Saved comparison composite!")
