import pdfplumber

pdf_path = "output/REK_IBNU_OKT_OUTPUT_1.pdf"
brain_dir = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098"

with pdfplumber.open(pdf_path) as pdf:
    # 1. Page 1 Header & Summary Box
    p1 = pdf.pages[0]
    crop_hdr = p1.crop((15, 80, 580, 260))
    crop_hdr.to_image(resolution=200).save(f"{brain_dir}/ibnu_okt_p1_header.png")
    
    # 2. Page 5 Salary (Tx 49, 25 Oct 2026 04:00:00 WIB, +6.300.000,00)
    p5 = pdf.pages[4]
    crop_sal = p5.crop((15, 270, 580, 480))
    crop_sal.to_image(resolution=200).save(f"{brain_dir}/ibnu_okt_p5_salary.png")
    
    # 3. Page 6 Closing (Tx 66, 31 Oct 2026 23:59:00 WIB, -5.000,00)
    p6 = pdf.pages[5]
    crop_cls = p6.crop((15, 450, 580, 680))
    crop_cls.to_image(resolution=200).save(f"{brain_dir}/ibnu_okt_p6_closing.png")

print("Saved October visual verification images!")
