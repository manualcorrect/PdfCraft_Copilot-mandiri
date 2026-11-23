import openpyxl
import pdfplumber

wb = openpyxl.load_workbook(r"output\Template_Mutasi_AUG_OUTPUT_1.xlsx", data_only=True)
ws = wb["Tabel_Mutasi"]
excel_data = []
for r in range(6, 64):
    excel_data.append({
        "no": ws.cell(r, 1).value,
        "date": str(ws.cell(r, 2).value),
        "time": str(ws.cell(r, 3).value),
        "nom": float(ws.cell(r, 5).value),
        "sal": float(ws.cell(r, 7).value) + 0.81
    })

def format_idr(num):
    return f"{abs(num):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

with pdfplumber.open(r"output\REK_KEISYA_AUG_OUTPUT_1.pdf") as pdf:
    pdf_txs = []
    for p_idx, page in enumerate(pdf.pages[:5]):
        words = page.extract_words()
        wibs = sorted([w for w in words if w["text"] == "WIB"], key=lambda x: x["top"])
        for w in wibs:
            s_words = [x for x in words if abs(x["top"] - w["top"]) < 15 and x["x0"] > 480]
            s_words.sort(key=lambda x: x["x0"])
            s_str = "".join([x["text"] for x in s_words])
            
            n_words = [x for x in words if abs(x["top"] - w["top"]) < 15 and 370 <= x["x0"] <= 450]
            n_words.sort(key=lambda x: x["x0"])
            n_str = "".join([x["text"] for x in n_words])
            
            d_words = [x for x in words if 0 < (w["top"] - x["top"]) < 15 and 45 <= x["x0"] <= 95]
            d_words.sort(key=lambda x: x["x0"])
            d_str = " ".join([x["text"] for x in d_words])
            
            t_candidates = [x for x in words if abs(x["top"] - w["top"]) < 3 and x["x1"] <= w["x0"] + 1]
            t_str = t_candidates[-1]["text"] + " WIB" if t_candidates else "12:00:00 WIB"
            
            no_words = [x for x in words if abs(x["top"] - w["top"]) < 15 and 15 <= x["x0"] <= 35]
            no_str = no_words[0]["text"] if no_words else "?"
            
            pdf_txs.append({
                "no": no_str,
                "date": d_str,
                "time": t_str,
                "nom": n_str,
                "sal": s_str
            })

print(f"Comparing {len(pdf_txs)} PDF rows vs {len(excel_data)} Excel rows:")
mismatches = 0
for i in range(58):
    p = pdf_txs[i]
    e = excel_data[i]
    e_sal_str = format_idr(e["sal"])
    e_nom_str = ("+" if e["nom"] > 0 else "-") + format_idr(e["nom"])
    
    if p["sal"] != e_sal_str:
        print(f"Row {i+1} SALDO MISMATCH: PDF={p['sal']} vs Excel={e_sal_str}")
        mismatches += 1
    if p["nom"] != e_nom_str:
        print(f"Row {i+1} NOMINAL MISMATCH: PDF={p['nom']} vs Excel={e_nom_str}")
        mismatches += 1
    if p["time"] != e["time"]:
        print(f"Row {i+1} TIME MISMATCH: PDF={p['time']} vs Excel={e['time']}")
        mismatches += 1

if mismatches == 0:
    print("ALL 58 ROWS PERFECTLY MATCH IN PDF AND EXCEL! 100% AUDIT KLOP!")
else:
    print(f"Total mismatches: {mismatches}")
