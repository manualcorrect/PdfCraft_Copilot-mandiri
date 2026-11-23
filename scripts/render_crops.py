import pdfplumber

pdf_path = "output/REK_IBNU_SEP_OUTPUT_1.pdf"
brain_dir = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098"

with pdfplumber.open(pdf_path) as pdf:
    # Page 6 (Tx 59 - 70)
    p6 = pdf.pages[5]
    crop_salary = p6.crop((15, 200, 580, 420))
    crop_salary.to_image(resolution=200).save(f"{brain_dir}/ibnu_sep_p6_salary_verified.png")
    
    # Page 7 (Tx 71 - 82)
    p7 = pdf.pages[6]
    crop_closing = p7.crop((15, 450, 580, 750))
    crop_closing.to_image(resolution=200).save(f"{brain_dir}/ibnu_sep_p7_closing_verified.png")

print("Saved salary and closing visual crops!")
