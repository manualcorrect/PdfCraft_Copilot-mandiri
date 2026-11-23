import pdfplumber

def dump_page_words(pdf_path, page_num):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num - 1]
        words = page.extract_words()
        return words

user_aug = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\REK_GALANG_AUG.pdf'
broken_out = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_OUTPUT_1.pdf'
ref_pdf = r'templates\master_page_1.pdf'

w_user = dump_page_words(user_aug, 1)
w_broken = dump_page_words(broken_out, 1)
w_ref = dump_page_words(ref_pdf, 1)

print(f"Total words on P1:")
print(f"  User REK_GALANG_AUG.pdf   : {len(w_user)} words")
print(f"  Broken REK_GALANG_AUG_OUTPUT_1: {len(w_broken)} words")
print(f"  Reference master_page_1.pdf : {len(w_ref)} words")

print("\n--- Summary Block Comparison (top 140 to 220) ---")
print("User AUG Summary:")
for w in sorted([w for w in w_user if 135 <= w['top'] <= 225 and w['x0'] > 450], key=lambda x: (x['top'], x['x0'])):
    print(f"  {w['text']:20s} at top={w['top']:.1f}, x0={w['x0']:.1f}")

print("\nBroken OUTPUT_1 Summary:")
for w in sorted([w for w in w_broken if 135 <= w['top'] <= 225 and w['x0'] > 450], key=lambda x: (x['top'], x['x0'])):
    print(f"  {w['text']:20s} at top={w['top']:.1f}, x0={w['x0']:.1f}")

print("\n--- Table Rows Comparison (Rows 1 to 5) ---")
print("User AUG Rows 1-3:")
for w in sorted([w for w in w_user if 320 <= w['top'] <= 460], key=lambda x: (x['top'], x['x0'])):
    print(f"  {w['text']:25s} at top={w['top']:.1f}, x0={w['x0']:.1f}")

print("\nBroken OUTPUT_1 Rows 1-3:")
for w in sorted([w for w in w_broken if 320 <= w['top'] <= 460], key=lambda x: (x['top'], x['x0'])):
    print(f"  {w['text']:25s} at top={w['top']:.1f}, x0={w['x0']:.1f}")
