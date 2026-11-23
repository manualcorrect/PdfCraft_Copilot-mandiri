import pdfplumber

pdf_path = "output/REK_IBNU_SEP_OUTPUT_1.pdf"
brain_dir = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098"

with pdfplumber.open(pdf_path) as pdf:
    # 1. Summary box crop
    p1 = pdf.pages[0]
    crop_sb = p1.crop((280, 160, 580, 260))
    im_sb = crop_sb.to_image(resolution=300)
    im_sb.save(f"{brain_dir}/ibnu_sep_summary_box.png")
    print(f"Saved: {brain_dir}/ibnu_sep_summary_box.png")

    # 2. Page 1 Header crop
    crop_hdr = p1.crop((15, 80, 580, 260))
    im_hdr = crop_hdr.to_image(resolution=200)
    im_hdr.save(f"{brain_dir}/ibnu_sep_p1_header.png")
    print(f"Saved: {brain_dir}/ibnu_sep_p1_header.png")

    # 3. Page 6 Salary crop (Tx 62)
    p6 = pdf.pages[5]
    crop_p6 = p6.crop((15, 260, 580, 400))
    im_p6 = crop_p6.to_image(resolution=200)
    im_p6.save(f"{brain_dir}/ibnu_sep_p6_salary.png")
    print(f"Saved: {brain_dir}/ibnu_sep_p6_salary.png")

    # 4. Page 7 Closing Fee crop (Tx 82)
    p7 = pdf.pages[6]
    crop_p7 = p7.crop((15, 620, 580, 770))
    im_p7 = crop_p7.to_image(resolution=200)
    im_p7.save(f"{brain_dir}/ibnu_sep_p7_closing.png")
    print(f"Saved: {brain_dir}/ibnu_sep_p7_closing.png")
