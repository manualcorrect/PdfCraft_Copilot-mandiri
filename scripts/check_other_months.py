import pdfplumber

sep_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\sep\REK_KEISYA_SEP_OUTPUT_1.pdf"
okt_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt\REK_KEISYA_OKT_OUTPUT_1.pdf"

def check_file(path, label):
    print(f"\n--- {label} ---")
    with pdfplumber.open(path) as pdf:
        chars = [c for c in pdf.pages[0].chars if 205 <= c['top'] <= 226 and c['x0'] > 280]
        # print first 3 and last 3
        chars.sort(key=lambda c: c['x0'])
        for c in chars[:4] + chars[-4:]:
            print(f"  '{c['text']}' top={c['top']:.4f}, y0={c['y0']:.4f}, x0={c['x0']:.4f}")

check_file(sep_pdf, "SEPTEMBER OUTPUT 1")
check_file(okt_pdf, "OCTOBER OUTPUT 1")
