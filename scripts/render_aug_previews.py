import sys
import os
import shutil
import base64

sys.path.insert(0, os.path.abspath("src"))
from pdfcraft_client import PdfCraftClient
from PIL import Image

pdf_path = "output/test_fix_edited_pdf.pdf"
out_dir = "C:/Users/Wisnu/.gemini/antigravity/brain/5e8306ab-a513-43f6-bf81-265c0e523098"

with PdfCraftClient() as client:
    doc = client.doc_open(pdf_path)
    for p in range(1, 5):
        res = client.call_tool("page_render", {"doc": doc, "page": p, "dpi": 150})
        b64_data = res["content"][0]["data"]
        img_path = f"{out_dir}/aug_preview_p{p}.png"
        with open(img_path, "wb") as f:
            f.write(base64.b64decode(b64_data))
        print(f"Rendered Page {p} -> {img_path}")
    client.doc_close(doc)

# Let's also crop the key areas:
# 1. Page 1 Header & Acc Num
p1_img = Image.open(f"{out_dir}/aug_preview_p1.png")
w, h = p1_img.size
crop_p1_header = p1_img.crop((0, 0, w, int(h * 0.40)))
crop_p1_header.save(f"{out_dir}/aug_p1_header_crop.png")

# 2. Page 2 Rows (showing Tx 22 Salary)
p2_img = Image.open(f"{out_dir}/aug_preview_p2.png")
crop_p2_gaji = p2_img.crop((0, int(h * 0.70), w, h))
crop_p2_gaji.save(f"{out_dir}/aug_p2_gaji_crop.png")

# 3. Page 3 Rows (showing chronological dates: 25 Aug, 26 Aug, 27 Aug)
p3_img = Image.open(f"{out_dir}/aug_preview_p3.png")
crop_p3_dates = p3_img.crop((0, int(h * 0.18), w, int(h * 0.65)))
crop_p3_dates.save(f"{out_dir}/aug_p3_dates_crop.png")

print("All preview crops created successfully!")
