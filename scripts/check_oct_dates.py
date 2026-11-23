import pdfplumber
import re

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\Folder Baru (2)\Folder Baru\OCT\1.pdf") as pdf:
    tx_i = 1
    for p_idx, page in enumerate(pdf.pages):
        words = page.extract_words()
        wibs = sorted([w for w in words if w["text"] == "WIB"], key=lambda x: x["top"])
        for w in wibs:
            time_w = [x["text"] for x in words if abs(x["top"] - w["top"]) < 3 and x["x1"] <= w["x0"] + 1]
            t_str = f"{time_w[-1]} WIB" if time_w else ""
            date_w = [x["text"] for x in words if 0 < (w["top"] - x["top"]) < 15 and 45 <= x["x0"] <= 95]
            raw_d = " ".join(date_w).strip()
            print(f"Tx {tx_i:2d} (Page {p_idx+1}): Date='{raw_d}' | Time='{t_str}'")
            tx_i += 1
