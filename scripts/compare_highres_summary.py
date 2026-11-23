import os
import pypdfium2 as pdfium
from PIL import Image

aug_dir = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug"
p_orig = os.path.join(aug_dir, "0.pdf")
p_out = os.path.join(aug_dir, "REK_KEISYA_AUG_OUTPUT_1.pdf")

doc_orig = pdfium.PdfDocument(p_orig)
doc_out = pdfium.PdfDocument(p_out)

im_orig = doc_orig[0].render(scale=3.0).to_pil()
im_out = doc_out[0].render(scale=3.0).to_pil()

# Crop summary box: y is from 150 to 260 pt -> in scale 3, y is 450 to 780
# x is from 280 to 580 pt -> in scale 3, x is 840 to 1740
box = (840, 450, 1750, 780)
crop_orig = im_orig.crop(box)
crop_out = im_out.crop(box)

out_dir = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098"
crop_orig.save(os.path.join(out_dir, "highres_orig_summary.png"))
crop_out.save(os.path.join(out_dir, "highres_out_summary.png"))
print("Saved highres_orig_summary.png and highres_out_summary.png!")
