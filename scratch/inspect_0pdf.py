import pdfplumber

pdf_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Wafiq\Folder Baru\aug\0.pdf"
with pdfplumber.open(pdf_path) as pdf:
    for i, p in enumerate(pdf.pages):
        print(f"=== PAGE {i+1} ===")
        words = p.extract_words()
        top_words = [w for w in words if w["top"] < 150]
        print("Header words (top < 150):")
        print(" ".join(w["text"] for w in sorted(top_words, key=lambda x: (x["top"], x["x0"]))))
        if i == 0:
            sum_words = [w for w in words if 150 <= w["top"] <= 270]
            print("Summary words (150 <= top <= 270):")
            for w in sorted(sum_words, key=lambda x: (x["top"], x["x0"])):
                print(f"  {w['text']} at x={w['x0']:.1f}, top={w['top']:.1f}")
