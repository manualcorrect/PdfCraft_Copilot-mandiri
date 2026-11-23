import pdfplumber

with pdfplumber.open(r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ibnu Agun\Folder Baru\aug\0.pdf") as pdf:
    for p_idx in range(len(pdf.pages)):
        p = pdf.pages[p_idx]
        sals = [c for c in p.chars if 500 <= c['x0'] <= 580 and c['text'] == '1'] # last digit of saldo ,81
        if sals:
            last_c = sorted(sals, key=lambda x: x['x1'])[-1]
            print(f"Page {p_idx+1}: last char x1 = {last_c['x1']:.2f}")
