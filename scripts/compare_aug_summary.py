import os
import pdfplumber

aug_dir = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug"
p_orig = os.path.join(aug_dir, "0.pdf")
p_out = os.path.join(aug_dir, "REK_KEISYA_AUG_OUTPUT_1.pdf")

print("--- 0.PDF (Original Basis in AUG) ---")
with pdfplumber.open(p_orig) as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    summary_words = [w for w in words if 150 <= w['top'] <= 260 and w['x0'] > 280]
    summary_words.sort(key=lambda w: (w['top'], w['x0']))
    for w in summary_words:
        print(f"  {w['text']:<35} top={w['top']:.2f}, bottom={w['bottom']:.2f}, x0={w['x0']:.2f}, x1={w['x1']:.2f}")

print("\n--- REK_KEISYA_AUG_OUTPUT_1.PDF ---")
with pdfplumber.open(p_out) as pdf:
    p1 = pdf.pages[0]
    words = p1.extract_words()
    summary_words = [w for w in words if 150 <= w['top'] <= 260 and w['x0'] > 280]
    summary_words.sort(key=lambda w: (w['top'], w['x0']))
    for w in summary_words:
        print(f"  {w['text']:<35} top={w['top']:.2f}, bottom={w['bottom']:.2f}, x0={w['x0']:.2f}, x1={w['x1']:.2f}")
