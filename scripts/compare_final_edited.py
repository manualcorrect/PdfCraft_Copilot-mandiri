import pdfplumber

aug_final = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_FINAL.pdf"
aug_edited = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_edited ketengangan.pdf"

print("--- COMPARING FINAL vs EDITED KETERANGAN ---")
with pdfplumber.open(aug_final) as pdf_f, pdfplumber.open(aug_edited) as pdf_e:
    for p_idx in range(len(pdf_f.pages)):
        pf = pdf_f.pages[p_idx]
        pe = pdf_e.pages[p_idx]
        
        words_f = pf.extract_words()
        words_e = pe.extract_words()
        
        wibs_f = sorted([w for w in words_f if w["text"] == "WIB" and w["top"] > 200], key=lambda x: x["top"])
        wibs_e = sorted([w for w in words_e if w["text"] == "WIB" and w["top"] > 200], key=lambda x: x["top"])
        
        print(f"\n--- PAGE {p_idx+1} (Rows: final={len(wibs_f)}, edited={len(wibs_e)}) ---")
        for i in range(len(wibs_e)):
            we = wibs_e[i]
            # get edited row text
            kw_e = [w for w in words_e if 95 <= w["x0"] <= 370 and (we["top"] - 15) <= w["top"] <= (we["top"] + 32)]
            txt_e = " ".join([w["text"] for w in kw_e])
            
            txt_f = ""
            if i < len(wibs_f):
                wf = wibs_f[i]
                kw_f = [w for w in words_f if 95 <= w["x0"] <= 370 and (wf["top"] - 15) <= w["top"] <= (wf["top"] + 32)]
                txt_f = " ".join([w["text"] for w in kw_f])
            
            diff = "SAME" if txt_e == txt_f else "DIFFERENT!"
            print(f"Row {i+1:2d} [{diff}]:")
            if diff == "DIFFERENT!":
                print(f"   FINAL : {txt_f}")
                print(f"   EDITED: {txt_e}")
