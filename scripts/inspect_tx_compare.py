import pdfplumber

def inspect_tx(pdf_path, page_num):
    print(f"=== {pdf_path} (Page {page_num}) ===")
    with pdfplumber.open(pdf_path) as pdf:
        p = pdf.pages[page_num - 1]
        words = p.extract_words()
        for w in sorted(words, key=lambda x: (x['top'], x['x0'])):
            if (250 <= w['top'] <= 300) or (680 <= w['top'] <= 750):
                print(f"{w['top']:.2f}, {w['x0']:.2f}-{w['x1']:.2f}: {w['text']}")

print("--- REK_WAFIQ_AUG_OUTPUT_PERFECT.pdf PAGE 3 ---")
inspect_tx(r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\REK_WAFIQ_AUG_OUTPUT_PERFECT.pdf', 3)
