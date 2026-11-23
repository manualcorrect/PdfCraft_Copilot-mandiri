import pdfplumber

nasih_path = r'D:\X_Files\rekening\Reference\nasih 2024 new unlocked\ilovepdf_unlocked\e-Statement_XXXXXXXXX9210_01 Des 2024-31 Des 2024_unlocked.pdf'
roy_path = r'D:\X_Files\rekening\Reference\Roy\ilovepdf_unlocked\Agu 2026_unlocked.pdf'

for name, path in [('Nasih', nasih_path), ('Roy', roy_path)]:
    with pdfplumber.open(path) as pdf:
        print(f"=== {name} Page Numbers ===")
        for i, page in enumerate(pdf.pages[:3]):
            words = [w for w in page.extract_words() if w['top'] < 130 and ('dari' in w['text'] or 'of' in w['text'] or (w['text'].isdigit() and w['x0'] > 500))]
            print(f"Page {i+1}:")
            for w in words:
                print(f"  {w['text']:8} x0={w['x0']:6.2f} x1={w['x1']:6.2f} top={w['top']:6.2f} bottom={w['bottom']:6.2f}")
