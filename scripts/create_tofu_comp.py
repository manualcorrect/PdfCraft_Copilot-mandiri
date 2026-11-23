from PIL import Image, ImageDraw

brain_dir = r'C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098'

# Load user screenshot
user_img = Image.open(f"{brain_dir}/.user_uploaded/media_1794541080193_0f8976a1.jpg")
# The summary box in user screenshot:
# User screen size is 1920x1080
# Let's crop the summary box region from user screen
# In user screenshot:
# Tabungan NOW IDR is at x~500, y~430
# Summary box is around x: 1080 to 1690, y: 430 to 620
w_u, h_u = user_img.size
# Let's crop proportionally:
crop_u = user_img.crop((int(w_u * 0.55), int(h_u * 0.42), int(w_u * 0.88), int(h_u * 0.63)))

fixed_img = Image.open(f"{brain_dir}/sb_crop_aug_fixed_slash.png")
ref_img = Image.open(f"{brain_dir}/sb_crop_ref.png")

# Resize crop_u to match height of fixed_img
target_h = fixed_img.height
crop_u_resized = crop_u.resize((int(crop_u.width * target_h / crop_u.height), target_h))
ref_resized = ref_img.resize((int(ref_img.width * target_h / ref_img.height), target_h))

total_w = crop_u_resized.width + fixed_img.width + ref_resized.width + 40
comp = Image.new('RGB', (total_w, target_h + 60), (255, 255, 255))
draw = ImageDraw.Draw(comp)

x_cursor = 10
comp.paste(crop_u_resized, (x_cursor, 50))
draw.text((x_cursor + 10, 15), "ERROR SEBELUMNYA (Kotak Tofu '/' di Font Italic)", fill=(200, 0, 0))

x_cursor += crop_u_resized.width + 10
comp.paste(fixed_img, (x_cursor, 50))
draw.text((x_cursor + 10, 15), "HASIL PERBAIKAN (Slash '/' di Font Bold, 100% Sempurna)", fill=(0, 150, 0))

x_cursor += fixed_img.width + 10
comp.paste(ref_resized, (x_cursor, 50))
draw.text((x_cursor + 10, 15), "FILE REFERENSI ASLI MANDIRI", fill=(0, 0, 150))

comp.save(f"{brain_dir}/tofu_fix_comparison.png")
print("Saved tofu_fix_comparison.png!")
