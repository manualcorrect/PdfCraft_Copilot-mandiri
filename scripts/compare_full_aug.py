import pdfplumber

aug_final = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_FINAL.pdf"
aug_edited = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_edited ketengangan.pdf"

print("--- FULL COMPARISON: FINAL vs EDITED ---")
with pdfplumber.open(aug_final) as pf, pdfplumber.open(aug_edited) as pe:
    # 1. Compare Page 1 Header
    p1_f = pf.pages[0].extract_words()
    p1_e = pe.pages[0].extract_words()
    
    # Check headers
    for label in ["GALANG", "Ciceri", "01 Aug", "09 Sep", "1630016287487", "4.530.335,81", "7.649.000,00", "7.651.988,00", "4.527.347,81"]:
        wf = [w for w in p1_f if label in w["text"]]
        we = [w for w in p1_e if label in w["text"]]
        print(f"Header '{label}': final={'FOUND' if wf else 'MISSING'}, edited={'FOUND' if we else 'MISSING'}")

    # 2. Compare Nominals and Saldos across all 4 pages
    for p_idx in range(4):
        wf = pf.pages[p_idx].extract_words()
        we = pe.pages[p_idx].extract_words()
        
        # Nominal words: x0 between 370 and 450
        noms_f = [w["text"] for w in sorted(wf, key=lambda x: x["top"]) if 370 <= w["x0"] <= 450 and w["top"] > 200]
        noms_e = [w["text"] for w in sorted(we, key=lambda x: x["top"]) if 370 <= w["x0"] <= 450 and w["top"] > 200]
        
        # Saldo words: x0 between 480 and 585
        sals_f = [w["text"] for w in sorted(wf, key=lambda x: x["top"]) if 480 <= w["x0"] <= 585 and w["top"] > 200]
        sals_e = [w["text"] for w in sorted(we, key=lambda x: x["top"]) if 480 <= w["x0"] <= 585 and w["top"] > 200]
        
        print(f"\nPage {p_idx+1}:")
        print(f"  Nominals match: {noms_f == noms_e} (counts: final={len(noms_f)}, edited={len(noms_e)})")
        if noms_f != noms_e:
            print(f"    noms_f: {noms_f}")
            print(f"    noms_e: {noms_e}")
        print(f"  Saldos match: {sals_f == sals_e} (counts: final={len(sals_f)}, edited={len(sals_e)})")
        if sals_f != sals_e:
            print(f"    sals_f: {sals_f}")
            print(f"    sals_e: {sals_e}")
