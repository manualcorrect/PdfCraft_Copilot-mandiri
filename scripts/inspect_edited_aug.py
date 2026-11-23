import pdfplumber
import openpyxl

aug_edited = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\REK_GALANG_AUG_2026_edited ketengangan.pdf"
ref_2 = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\2.pdf"
excel_path = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\AUG\Template_Mutasi_Aug.xlsx"

print("--- EXAMINING REK_GALANG_AUG_2026_edited ketengangan.pdf ---")
with pdfplumber.open(aug_edited) as pdf:
    for p_num, page in enumerate(pdf.pages, 1):
        words = page.extract_words()
        # Find all words with WIB
        wibs = sorted([w for w in words if w["text"] == "WIB" and w["top"] > 200], key=lambda x: x["top"])
        print(f"\nPage {p_num}: {len(wibs)} transaction rows detected")
        for i, w in enumerate(wibs):
            # date above WIB
            dates = [d["text"] for d in words if 0 < (w["top"] - d["top"]) < 15 and 45 <= d["x0"] <= 95]
            time_w = [t["text"] for t in words if abs(t["top"] - w["top"]) < 3 and t["x1"] <= w["x0"] + 1]
            date_str = " ".join(dates)
            time_str = " ".join(time_w) + " WIB"
            
            # keterangan words roughly between x0=100 and x1=370, top near w['top']
            # row vertical span is roughly top: w['top'] - 15 to w['top'] + 30
            ket_words = [k for k in words if 95 <= k["x0"] <= 370 and (w["top"] - 15) <= k["top"] <= (w["top"] + 32)]
            # group by line
            ket_text = " ".join([k["text"] for k in sorted(ket_words, key=lambda x: (x["top"] // 5, x["x0"]))])
            
            # nominal around x0=370 to 450
            nom_words = [n["text"] for n in words if 370 <= n["x0"] <= 450 and abs(n["top"] - (w["top"] - 3)) < 15]
            nom_str = " ".join(nom_words)

            # saldo around x0=480 to 580
            sal_words = [s["text"] for s in words if 480 <= s["x0"] <= 585 and abs(s["top"] - (w["top"] - 3)) < 15]
            sal_str = " ".join(sal_words)

            print(f"Row {i+1:2d} | Top={w['top']:6.1f} | Date={date_str:<12} | Time={time_str:<12} | Nom={nom_str:<15} | Sal={sal_str:<15} | Ket={ket_text[:40]}")
