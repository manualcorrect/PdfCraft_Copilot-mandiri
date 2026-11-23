import pdfplumber

with pdfplumber.open("output/REK_GALANG_OCT_2026_CHRONOLOGICAL.pdf") as pdf:
    print("Total pages:", len(pdf.pages))
    for p_idx, page in enumerate(pdf.pages):
        print(f"\n{'='*20} PAGE {p_idx+1} {'='*20}")
        text = page.extract_text()
        print(text[:400] if text else "EMPTY PAGE")
        
        # Check for any suspicious characters like \x00, ?, box, tofu
        for c in page.chars:
            t = c['text']
            if ord(t) > 127 and t not in ['\xa0']:
                print(f"Non-ascii char: {repr(t)} (ord={ord(t)}) at x={c['x0']:.1f}, top={c['top']:.1f}")
            if c.get('adv') == 8.0 and t in ['c', 'k', 't', 'O']:
                print(f"Suspicious 8.0 width char: {repr(t)} at x={c['x0']:.1f}, top={c['top']:.1f}")
