import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\REK_KEISYA_SEP_OUTPUT_1.pdf") as pdf:
    p1 = pdf.pages[0]
    crop = p1.crop((120, 115, 220, 135))
    im = crop.to_image(resolution=300)
    im.save(r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\keisya_sep_branch_crop.png")
