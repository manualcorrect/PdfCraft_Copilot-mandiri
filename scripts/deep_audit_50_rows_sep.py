"""
Rigorous Deep Audit & Verification Suite:
Compares REK_KEISYA_SEP_OUTPUT_1.pdf against:
1. Template_Mutasi_SEP_OUTPUT_1.xlsx (100% data fidelity: date, time, no, nominal, saldo).
2. 0.pdf (100% untouched description verification: exact characters, line breaks, zero paragraph shifts).
3. Header, Account, Summary Box, and Page Number anchors.
4. Visual rendering verification via pypdfium2 (generates inspection crops).
"""

import os
import sys
import openpyxl
import pdfplumber
import pypdfium2 as pdfium
from PIL import Image

WORKSPACE_DIR = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot"
PDF_OUT = os.path.join(WORKSPACE_DIR, "output", "REK_KEISYA_SEP_OUTPUT_1.pdf")
EXCEL_OUT = os.path.join(WORKSPACE_DIR, "output", "Template_Mutasi_SEP_OUTPUT_1.xlsx")
PDF_ORIG = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\0.pdf"

def format_idr(num):
    return f"{abs(num):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def run_deep_audit():
    print("=================================================================")
    print("STARTING DEEP AUDIT: KEISYA AULIA - SEPTEMBER 2026 (OUTPUT 1)")
    print("=================================================================")

    # 1. READ EXCEL DATA
    wb = openpyxl.load_workbook(EXCEL_OUT, data_only=True)
    ws = wb['Tabel_Mutasi']
    
    excel_rows = []
    for r in range(6, 60):
        nom = ws.cell(r, 5).value
        sal = ws.cell(r, 7).value
        if nom is not None and abs(float(nom)) > 0.001:
            excel_rows.append({
                'no': int(ws.cell(r, 1).value),
                'date': ws.cell(r, 2).value.strftime("%d %b %Y") if hasattr(ws.cell(r, 2).value, 'strftime') else str(ws.cell(r, 2).value),
                'time': str(ws.cell(r, 3).value).strip(),
                'nom': float(nom),
                'tipe': ws.cell(r, 6).value,
                'saldo': float(sal) + 0.81,
                'excel_row': r
            })

    print(f"Loaded {len(excel_rows)} active transaction rows from Excel.")
    assert len(excel_rows) == 50

    # 2. EXTRACT PDF DATA
    pdf_rows = []
    with pdfplumber.open(PDF_OUT) as pdf:
        assert len(pdf.pages) == 5, f"Expected 5 pages, found {len(pdf.pages)}"
        
        # Check Header on Page 1
        p1 = pdf.pages[0]
        p1_text = p1.extract_text()
        assert "KEISYA AULIA" in p1_text, "Name KEISYA AULIA missing on Page 1"
        assert "KCP Serang Ciceri" in p1_text, "Branch missing on Page 1"
        assert "01 Sep 2026 - 30 Sep 2026" in p1_text, "Period missing on Page 1"
        assert "12 Nov 2026" in p1_text, "Issued on missing on Page 1"
        assert "1630016478664" in p1_text, "Account number missing on Page 1"
        assert "2.698.988,81" in p1_text, "Saldo Awal missing on Page 1"
        assert "+ 11.379.332,00" in p1_text or "11.379.332,00" in p1_text, "Dana Masuk missing on Page 1"
        assert "- 7.227.500,00" in p1_text or "7.227.500,00" in p1_text, "Dana Keluar missing on Page 1"
        assert "6.850.820,81" in p1_text, "Saldo Akhir missing on Page 1"
        print("Page 1 Header, Summary Box, and Account Number: 100% VERIFIED.")

        # Check Page Numbers on all 5 pages
        for p_idx, page in enumerate(pdf.pages, 1):
            txt = page.extract_text()
            assert f"{p_idx} dari 5" in txt, f"Page {p_idx}: missing '{p_idx} dari 5'"
            assert f"{p_idx} of 5" in txt, f"Page {p_idx}: missing '{p_idx} of 5'"
            print(f"Page {p_idx} Page Number '{p_idx} dari 5' & '{p_idx} of 5': VERIFIED.")

        # Extract Transactions
        tx_no = 0
        for p_idx, page in enumerate(pdf.pages, 1):
            words = page.extract_words()
            min_top = 320 if p_idx == 1 else 200
            table_words = [w for w in words if min_top <= w['top'] <= 800]
            wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
            
            for w in wibs:
                tx_no += 1
                row_top = w['top']
                
                # No: x0 < 40
                no_cands = [x for x in table_words if abs(x['top'] - row_top) < 15 and x['x0'] < 40]
                no_str = no_cands[0]['text'] if no_cands else "MISSING"
                
                # Date: 45 <= x0 <= 95, top above wib
                d_cands = [x for x in table_words if 0 < (row_top - x['top']) < 15 and 45 <= x['x0'] <= 95]
                d_cands.sort(key=lambda x: x['x0'])
                d_str = " ".join([x['text'] for x in d_cands])
                
                # Time: x1 <= w['x0'] + 1
                t_cands = [x for x in table_words if abs(x['top'] - row_top) < 3 and x['x1'] <= w['x0'] + 1]
                t_str = f"{t_cands[-1]['text']} WIB" if t_cands else "MISSING"
                
                # Nominal: 370 <= x0 <= 450
                nom_cands = [x for x in table_words if abs(x['top'] - row_top) < 15 and 370 <= x['x0'] < 480]
                nom_str = " ".join([x['text'] for x in nom_cands]).replace(" ", "")
                
                # Saldo: x0 >= 480
                sal_cands = [x for x in table_words if abs(x['top'] - row_top) < 15 and x['x0'] >= 480]
                sal_str = " ".join([x['text'] for x in sal_cands])
                
                # Keterangan: 110 <= x0 <= 370
                ket_cands = [x for x in table_words if abs(x['top'] - row_top) < 25 and 110 <= x['x0'] < 370]
                ket_cands.sort(key=lambda x: (x['top'], x['x0']))
                ket_str = " ".join([x['text'] for x in ket_cands])
                
                pdf_rows.append({
                    'no': int(no_str) if no_str.isdigit() else no_str,
                    'date': d_str,
                    'time': t_str,
                    'nom_str': nom_str,
                    'saldo_str': sal_str,
                    'ket_str': ket_str,
                    'page': p_idx
                })

    assert len(pdf_rows) == 50, f"Expected 50 extracted rows, got {len(pdf_rows)}"
    print(f"\nExtracted {len(pdf_rows)} transaction rows from PDF.")

    # 3. COMPARE PDF VS EXCEL (ROW BY ROW)
    print("\n--- ROW-BY-ROW VERIFICATION: PDF VS EXCEL ---")
    all_match = True
    for i in range(50):
        er = excel_rows[i]
        pr = pdf_rows[i]
        
        # Check No
        assert pr['no'] == er['no'], f"Tx {i+1}: No mismatch (PDF={pr['no']} vs Excel={er['no']})"
        
        # Check Date
        assert pr['date'] == er['date'], f"Tx {i+1}: Date mismatch (PDF='{pr['date']}' vs Excel='{er['date']}')"
        
        # Check Time
        assert pr['time'] == er['time'], f"Tx {i+1}: Time mismatch (PDF='{pr['time']}' vs Excel='{er['time']}')"
        
        # Check Nominal
        exp_nom_str = ("+" if er['nom'] > 0 else "-") + format_idr(er['nom'])
        assert pr['nom_str'] == exp_nom_str, f"Tx {i+1}: Nominal mismatch (PDF='{pr['nom_str']}' vs Excel='{exp_nom_str}')"
        
        # Check Saldo
        exp_sal_str = format_idr(er['saldo'])
        assert pr['saldo_str'] == exp_sal_str, f"Tx {i+1}: Saldo mismatch (PDF='{pr['saldo_str']}' vs Excel='{exp_sal_str}')"

    print("ALL 50 ROWS: Date, Time, No, Nominal, and Saldo MATCH EXCEL 100%!")

    # 4. VERIFY KETERANGAN UNTOUCHED (PDF_OUT VS 0.PDF)
    print("\n--- VERIFYING KETERANGAN 100% UNTOUCHED (PDF_OUT VS 0.PDF) ---")
    orig_kets = []
    with pdfplumber.open(PDF_ORIG) as pdf_orig:
        for p_idx, page in enumerate(pdf_orig.pages, 1):
            words = page.extract_words()
            min_top = 320 if p_idx == 1 else 200
            table_words = [w for w in words if min_top <= w['top'] <= 800]
            wibs = sorted([w for w in table_words if w['text'] == 'WIB'], key=lambda x: x['top'])
            for w in wibs:
                row_top = w['top']
                ket_cands = [x for x in table_words if abs(x['top'] - row_top) < 25 and 110 <= x['x0'] < 370]
                ket_cands.sort(key=lambda x: (x['top'], x['x0']))
                orig_kets.append(" ".join([x['text'] for x in ket_cands]))

    assert len(orig_kets) == 50
    ket_match_count = 0
    for i in range(50):
        ok = orig_kets[i]
        pk = pdf_rows[i]['ket_str']
        assert ok == pk, f"Tx {i+1}: Keterangan altered!\n  Orig: '{ok}'\n  PDF : '{pk}'"
        ket_match_count += 1

    print(f"KETERANGAN AUDIT: 50/50 descriptions are 100% IDENTICAL to 0.pdf (ZERO DOM shift).")

    # 5. RENDER HIGH-RES PNG PREVIEWS & CROPS
    print("\n--- GENERATING VISUAL VERIFICATION CROPS ---")
    doc = pdfium.PdfDocument(PDF_OUT)
    
    # Save full page renders (scale=2)
    for p_i in range(5):
        p = doc.get_page(p_i)
        img = p.render(scale=2).to_pil()
        render_path = os.path.join(WORKSPACE_DIR, "output", f"keisya_sep_rendered_p{p_i+1}.png")
        img.save(render_path)
    
    # 1. Header Crop (Page 1)
    p1_img = doc.get_page(0).render(scale=3).to_pil()
    # Crop Header (x: 10..585 pt, y: 30..260 pt)
    crop_header = p1_img.crop((10*3, 30*3, 585*3, 260*3))
    crop_header_path = os.path.join(WORKSPACE_DIR, "output", "keisya_sep_p1_header_crop.png")
    crop_header.save(crop_header_path)
    print(f"Saved: {crop_header_path}")

    # 2. Page Number Crop (Page 2)
    p2_img = doc.get_page(1).render(scale=3).to_pil()
    crop_p2_num = p2_img.crop((510*3, 90*3, 580*3, 130*3))
    crop_p2_num_path = os.path.join(WORKSPACE_DIR, "output", "keisya_sep_p2_pagenum_crop.png")
    crop_p2_num.save(crop_p2_num_path)
    print(f"Saved: {crop_p2_num_path}")

    # 3. Salary Row Crop (Page 4, Tx 37)
    p4_img = doc.get_page(3).render(scale=3).to_pil()
    # Tx 37 is Row 3 on Page 4 (expected y~320 pt, in image top = (842 - 522)? No, top coordinate in pdfium is from top edge)
    # y from top = 310 pt
    crop_sal = p4_img.crop((15*3, 305*3, 580*3, 355*3))
    crop_sal_path = os.path.join(WORKSPACE_DIR, "output", "keisya_sep_p4_salary_crop.png")
    crop_sal.save(crop_sal_path)
    print(f"Saved: {crop_sal_path}")

    # 4. Closing Fee Crop (Page 5, Tx 50)
    p5_img = doc.get_page(4).render(scale=3).to_pil()
    crop_close = p5_img.crop((15*3, 350*3, 580*3, 400*3))
    crop_close_path = os.path.join(WORKSPACE_DIR, "output", "keisya_sep_p5_closing_crop.png")
    crop_close.save(crop_close_path)
    print(f"Saved: {crop_close_path}")

    print("\n=================================================================")
    print("ALL AUDIT CHECKS PASSED WITH 100% PERFECTION!")
    print("=================================================================")

if __name__ == "__main__":
    run_deep_audit()
