import pdfplumber

ref_pdf = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf"
aug_0_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\0.pdf"

print("--- Checking aug/0.pdf ---")
with pdfplumber.open(aug_0_pdf) as pdf:
    for w in [w for w in pdf.pages[0].extract_words() if 200 <= w['top'] <= 230 and w['x0'] > 280]:
        print(f"  aug/0.pdf: {w['text']:<30} top={w['top']:.4f}, bottom={w['bottom']:.4f}, x0={w['x0']:.4f}, x1={w['x1']:.4f}")

print("\n--- Checking ref_pdf ---")
with pdfplumber.open(ref_pdf) as pdf:
    for w in [w for w in pdf.pages[0].extract_words() if 200 <= w['top'] <= 230 and w['x0'] > 280]:
        print(f"  ref_pdf:   {w['text']:<30} top={w['top']:.4f}, bottom={w['bottom']:.4f}, x0={w['x0']:.4f}, x1={w['x1']:.4f}")
