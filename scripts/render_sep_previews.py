import pypdfium2 as pdfium
import os

pdf_path = r"output\REK_GALANG_SEP_2026_PERFECT.pdf"
art_dir = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098"

doc = pdfium.PdfDocument(pdf_path)
print(f"Total pages: {len(doc)}")

for i in range(len(doc)):
    page = doc[i]
    # Render at 150 dpi (scale = 150 / 72 = 2.0833)
    image = page.render(scale=2.0).to_pil()
    out_name = f"sep_preview_p{i+1}.png"
    out_path = os.path.join(art_dir, out_name)
    image.save(out_path)
    print(f"Rendered Page {i+1} to {out_path} (size: {image.size})")

# Render close-up crops for verification:
# Crop 1: Page 1 Header & Account number
p1_img = doc[0].render(scale=2.0).to_pil()
# Crop Account number & Summary: rect around y in [160, 260], x in [10, 580]
# Scale 2 means y * 2, x * 2
p1_crop_header = p1_img.crop((20, 180, p1_img.width - 20, 520))
crop_h_path = os.path.join(art_dir, "sep_p1_header_crop.png")
p1_crop_header.save(crop_h_path)
print("Saved sep_p1_header_crop.png")

# Crop 2: Page 2 Gaji (Row 22)
p2_img = doc[1].render(scale=2.0).to_pil()
p2_crop_gaji = p2_img.crop((20, 1300, p2_img.width - 20, 1550))
crop_gaji_path = os.path.join(art_dir, "sep_p2_gaji_crop.png")
p2_crop_gaji.save(crop_gaji_path)
print("Saved sep_p2_gaji_crop.png")

# Crop 3: Page 4 Closing Row 35
p4_img = doc[3].render(scale=2.0).to_pil()
p4_crop_r35 = p4_img.crop((20, 360, p4_img.width - 20, 540))
crop_r35_path = os.path.join(art_dir, "sep_p4_row35_crop.png")
p4_crop_r35.save(crop_r35_path)
print("Saved sep_p4_row35_crop.png")
