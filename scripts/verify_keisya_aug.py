import pdfplumber, re, openpyxl

pdf_path = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\REK_KEISYA_AUG_OUTPUT_1.pdf"
excel_path = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\Template_Mutasi_AUG_OUTPUT_1.xlsx"

print("=== VERIFYING REK_KEISYA_AUG_OUTPUT_1.pdf ===")
with pdfplumber.open(pdf_path) as pdf:
    print(f"Total Pages: {len(pdf.pages)}")
    
    # 1. Fonts verification
    all_fonts = set()
    for p_idx, page in enumerate(pdf.pages):
        for c in page.chars:
            all_fonts.add(c.get('fontname', ''))
    print(f"All Fonts in PDF: {all_fonts}")
    foreign_fonts = [f for f in all_fonts if 'TTInterphases' not in f and 'Calibri' not in f]
    print(f"Foreign fonts (should be none): {foreign_fonts}")

    # 2. Page 1 Header & Summary
    p1 = pdf.pages[0]
    p1_text = p1.extract_text()
    print("\n--- Page 1 Header Checks ---")
    print("Contains 'KEISYA AULIA':", 'KEISYA AULIA' in p1_text)
    print("Contains 'KCP Serang Ciceri':", 'KCP Serang Ciceri' in p1_text)
    print("Contains '01 Aug 2026 - 31 Aug 2026':", '01 Aug 2026 - 31 Aug 2026' in p1_text)
    print("Contains '12 Nov 2026':", '12 Nov 2026' in p1_text)
    print("Contains '1630016478664':", '1630016478664' in p1_text)
    print("Contains '1 dari 6' or '1 dari6':", ('1 dari 6' in p1_text or '1 dari6' in p1_text))
    print("Contains '1 of 6':", '1 of 6' in p1_text)
    print("Contains '+ 11.950.000,00':", '+ 11.950.000,00' in p1_text)
    print("Contains '- 10.749.780,00':", '- 10.749.780,00' in p1_text)
    print("Contains '2.698.988,81':", '2.698.988,81' in p1_text)

    # 3. Check Intermediate Pages Headers
    for p_num in range(2, 6):
        pg = pdf.pages[p_num - 1]
        txt = pg.extract_text()
        print(f"\n--- Page {p_num} Header Checks ---")
        print(f"Contains 'KEISYA AULIA':", 'KEISYA AULIA' in txt)
        print(f"Contains '{p_num} dari 6':", (f'{p_num} dari 6' in txt or f'{p_num} dari6' in txt))
        print(f"Contains '{p_num} of 6':", (f'{p_num} of 6' in txt or f'{p_num}of 6' in txt))

    # 4. Check all 58 transactions chronological & format
    print("\n--- Transaction Rows Checks ---")
    tx_extracted = []
    for p_idx in range(5):
        page = pdf.pages[p_idx]
        words = page.extract_words()
        min_top = 320 if p_idx == 0 else 200
        table_words = [w for w in words if min_top <= w['top'] <= 800]
        wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
        for w in wibs:
            t_candidates = [x for x in table_words if abs(x['top'] - w['top']) < 3 and x['x1'] <= w['x0'] + 1]
            time_str = f"{t_candidates[-1]['text']} WIB" if t_candidates else "12:00:00 WIB"
            d_candidates = [x for x in table_words if 0 < (w['top'] - x['top']) < 15 and 45 <= x['x0'] <= 95]
            d_candidates.sort(key=lambda x: x['x0'])
            raw_d = " ".join([x['text'] for x in d_candidates]).strip()
            
            # Nom
            nom_c = [x for x in table_words if abs(x['top'] - w['top']) < 12 and 360 <= x['x0'] and x['x1'] <= 435]
            nom_str = nom_c[0]['text'] if nom_c else ""
            
            # Saldo
            sal_c = [x for x in table_words if abs(x['top'] - w['top']) < 12 and 450 <= x['x0'] and x['x1'] <= 575]
            sal_str = sal_c[0]['text'] if sal_c else ""
            
            tx_extracted.append({
                'date': raw_d,
                'time': time_str,
                'nom': nom_str,
                'sal': sal_str
            })

    print(f"Total transactions extracted from PDF: {len(tx_extracted)}")
    print("Row 1:", tx_extracted[0])
    print("Row 34 (Gaji):", tx_extracted[33])
    print("Row 58 (Closing):", tx_extracted[57])
    
    # Verify Mar is nowhere in transaction dates
    mar_found = [i+1 for i, t in enumerate(tx_extracted) if 'Mar' in t['date']]
    print("Any 'Mar' remaining in dates (should be []):", mar_found)

print("\n=== VERIFYING Template_Mutasi_AUG_OUTPUT_1.xlsx ===")
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Tabel_Mutasi']
empty_no = []
empty_tgl = []
empty_jam = []
for r in range(6, 64):
    if ws.cell(r, 1).value is None: empty_no.append(r)
    if ws.cell(r, 2).value is None: empty_tgl.append(r)
    if ws.cell(r, 3).value is None: empty_jam.append(r)

print(f"Empty No rows: {len(empty_no)}")
print(f"Empty Tanggal rows: {len(empty_tgl)}")
print(f"Empty Jam rows: {len(empty_jam)}")
print(f"Row 39 (Tx 34) Gaji in Excel: No={ws.cell(39, 1).value}, Tgl={ws.cell(39, 2).value}, Jam={ws.cell(39, 3).value}, Nom={ws.cell(39, 5).value}")
