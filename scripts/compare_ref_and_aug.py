import os
import pdfplumber

ref_pdf = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf"
aug_out_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\REK_KEISYA_AUG_OUTPUT_1.pdf"

print("==================================================")
print("COMPARING REFERENCE PDF vs REK_KEISYA_AUG_OUTPUT_1")
print("==================================================")

with pdfplumber.open(ref_pdf) as pdf_ref, pdfplumber.open(aug_out_pdf) as pdf_out:
    p1_ref = pdf_ref.pages[0]
    p1_out = pdf_out.pages[0]
    
    print("\n--- REFERENCE (Mar 2026 unlocked) - Page 1 words around summary (top 150..260) ---")
    words_ref = [w for w in p1_ref.extract_words() if 150 <= w['top'] <= 260 and w['x0'] > 280]
    words_ref.sort(key=lambda w: (w['top'], w['x0']))
    for w in words_ref:
        print(f"  {w['text']:<35} top={w['top']:.2f}, bottom={w['bottom']:.2f}, x0={w['x0']:.2f}, x1={w['x1']:.2f}")
        
    print("\n--- REK_KEISYA_AUG_OUTPUT_1 - Page 1 words around summary (top 150..260) ---")
    words_out = [w for w in p1_out.extract_words() if 150 <= w['top'] <= 260 and w['x0'] > 280]
    words_out.sort(key=lambda w: (w['top'], w['x0']))
    for w in words_out:
        print(f"  {w['text']:<35} top={w['top']:.2f}, bottom={w['bottom']:.2f}, x0={w['x0']:.2f}, x1={w['x1']:.2f}")
