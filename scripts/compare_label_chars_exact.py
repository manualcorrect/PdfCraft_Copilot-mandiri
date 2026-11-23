import pdfplumber

ref_pdf = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf"
aug_out_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\REK_KEISYA_AUG_OUTPUT_1.pdf"

with pdfplumber.open(ref_pdf) as p_ref, pdfplumber.open(aug_out_pdf) as p_out:
    c_ref = [c for c in p_ref.pages[0].chars if 205 <= c['top'] <= 226 and 290 <= c['x0'] <= 460]
    c_out = [c for c in p_out.pages[0].chars if 205 <= c['top'] <= 226 and 290 <= c['x0'] <= 460]
    
    print("Ref label chars:")
    for c in c_ref:
        print(f"'{c['text']}' x0={c['x0']:.2f}, y0={c['y0']:.2f}, top={c['top']:.2f} | ", end="")
    print("\n\nOut label chars:")
    for c in c_out:
        print(f"'{c['text']}' x0={c['x0']:.2f}, y0={c['y0']:.2f}, top={c['top']:.2f} | ", end="")
    print()
