import pdfplumber

ref_pdf = r"C:\Users\Wisnu\.gemini\antigravity\brain\5e8306ab-a513-43f6-bf81-265c0e523098\.user_uploaded\media_1794538873844_ae928147.pdf"
aug_out_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\aug\REK_KEISYA_AUG_OUTPUT_1.pdf"

print("=== DETAILED CHAR-BY-CHAR AUDIT FOR DANA KELUAR ROW ===")

def inspect_page1(path, name):
    print(f"\n--- {name} ---")
    with pdfplumber.open(path) as pdf:
        p = pdf.pages[0]
        chars = p.chars
        # filter chars around y = 205..225 pt (top)
        dk_chars = [c for c in chars if 205 <= c['top'] <= 226 and c['x0'] > 280]
        dk_chars.sort(key=lambda c: c['x0'])
        for c in dk_chars:
            print(f"  Char '{c['text']}' font={c.get('fontname')} size={c.get('size'):.2f} pt | top={c['top']:.4f}, bottom={c['bottom']:.4f}, y0={c['y0']:.4f}, y1={c['y1']:.4f}, x0={c['x0']:.4f}, x1={c['x1']:.4f}")

inspect_page1(ref_pdf, "REFERENCE (Mar 2026 unlocked)")
inspect_page1(aug_out_pdf, "AUGUST OUTPUT 1")
