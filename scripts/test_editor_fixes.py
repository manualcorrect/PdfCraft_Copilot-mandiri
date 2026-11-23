import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from pdfcraft_client import PdfCraftClient
from pdfcraft_editor import PdfCraftEditor
import pdfplumber

def main():
    src_pdf = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\Galang\REK GALANG AUG 2026.pdf"
    out_pdf = r"C:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\test_editor_result.pdf"

    # Make a fresh copy to work on
    with open(src_pdf, "rb") as f_in, open(out_pdf, "wb") as f_out:
        f_out.write(f_in.read())

    print(f"Testing PdfCraftEditor on fresh copy: {out_pdf}")

    with PdfCraftClient() as client:
        editor = PdfCraftEditor(client)
        doc_id = client.doc_open(out_pdf)
        print(f"Opened doc_id: {doc_id}")

        # 1. Fix financial summary on Page 1
        summary_res = editor.fix_financial_summary(doc_id, page=1)
        print(f"Fixed {len(summary_res)} financial summary items on Page 1.")

        # 2. Fix transaction table on Page 1 & 2
        p1_res = editor.fix_transaction_table(doc_id, page=1)
        print(f"Fixed {len(p1_res)} table values on Page 1.")

        p2_res = editor.fix_transaction_table(doc_id, page=2)
        print(f"Fixed {len(p2_res)} table values on Page 2.")

        # Save changes
        client.doc_save(doc_id)
        client.doc_close(doc_id)
        print("Saved and closed.")

    # Verification with pdfplumber
    print("\n--- Telemetry Verification with pdfplumber ---")
    with pdfplumber.open(out_pdf) as pdf:
        # Check summary right edges on Page 1
        p1 = pdf.pages[0]
        words = p1.extract_words()
        
        print("\n[Summary Block Verification (Target Right = 567.00 pt)]")
        for w in words:
            if any(k in w["text"] for k in ["5.285.348,00", "7.582.538,00", "6.719.364,00", "6.148.522,00"]):
                print(f"Summary: {w['text']:15s} | x0={w['x0']:.2f}, x1={w['x1']:.2f}, top={w['top']:.2f}")

        print("\n[Color Palette Verification]")
        for c in p1.chars:
            t = c["text"]
            if t in ["+", "-"]:
                col = c.get("non_stroking_color")
                print(f"Char '{t}' at ({c['x0']:.1f}, {c['top']:.1f}) color={col}")
            elif "5.285" in t:
                col = c.get("non_stroking_color")
                print(f"Initial Saldo char '{t}' color={col}")
            elif "6.148" in t:
                col = c.get("non_stroking_color")
                print(f"Closing Saldo char '{t}' color={col}")

if __name__ == "__main__":
    main()
