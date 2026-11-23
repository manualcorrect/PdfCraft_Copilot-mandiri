"""
PdfCraft Copilot - Main Execution CLI
Usage:
  python scripts/run_pipeline.py --excel templates/Template_Mutasi_Bank.xlsx --output output/REK_STANDARDIZED.pdf
  python scripts/run_pipeline.py --repair "D:\\...\\REK GALANG AUG 2026.pdf" --output output/REK_GALANG_AUG_2026_REPAIRED.pdf
  python scripts/run_pipeline.py --audit output/REK_STANDARDIZED.pdf
"""

import os
import sys
import argparse

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from statement_builder import StatementBuilder
from statement_doctor import StatementDoctor
import pdfplumber


def run_audit(pdf_path: str):
    """Audits the given PDF and outputs a comprehensive telemetry compliance report."""
    print(f"\n==========================================")
    print(f"   PDFCraft Copilot Telemetry Audit Report")
    print(f"   Target: {pdf_path}")
    print(f"==========================================")

    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        return

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total Pages: {total_pages}\n")

        for p_idx, page in enumerate(pdf.pages):
            p_num = p_idx + 1
            print(f"--- PAGE {p_num} AUDIT ---")
            
            # 1. Embedded Fonts
            fonts = set(c["fontname"] for c in page.chars)
            print(f"Fonts: {sorted(fonts)}")
            has_arial = any("Arial" in f for f in fonts)
            if has_arial:
                print("  [WARN] Page contains Arial fonts!")
            else:
                print("  [PASS] Pure authentic typography (no Arial).")

            words = page.extract_words()

            # 2. Financial Summary Block (Page 1 only)
            if p_num == 1:
                summary_words = [w for w in words if w["top"] < 260 and w["x0"] > 480]
                if summary_words:
                    print(f"  Financial Summary items: {len(summary_words)}")
                    for sw in summary_words:
                        dev = abs(sw["x1"] - 567.00)
                        print(f"    Summary: {sw['text']:16s} | x1={sw['x1']:.2f} pt (Target: 567.00 pt, dev: {dev:.2f} pt)")

            # 3. Table Right-edge alignments
            min_y = 320 if p_num == 1 else 200
            table_words = [w for w in words if min_y <= w["top"] <= 800]
            
            table_nominals = [w for w in table_words if (w["text"].startswith("+") or w["text"].startswith("-")) and 360 <= w["x0"] <= 440]
            if table_nominals:
                nom_devs = [abs(w["x1"] - 432.00) for w in table_nominals]
                print(f"  Table Nominals (Target: 432.00 pt, Count: {len(table_nominals)}):")
                print(f"    Avg dev: {sum(nom_devs)/len(nom_devs):.2f} pt | Max dev: {max(nom_devs):.2f} pt")

            table_saldos = [w for w in table_words if 500 <= w["x0"] <= 580 and "," in w["text"]]
            if table_saldos:
                saldo_devs = [abs(w["x1"] - 571.00) for w in table_saldos]
                print(f"  Table Saldos   (Target: 571.00 pt, Count: {len(table_saldos)}):")
                print(f"    Avg dev: {sum(saldo_devs)/len(saldo_devs):.2f} pt | Max dev: {max(saldo_devs):.2f} pt")

            # 4. Check Colors
            green_chars = [c for c in page.chars if c.get("non_stroking_color") == (0.0235, 0.6667, 0.4353)]
            blue_chars = [c for c in page.chars if c.get("non_stroking_color") == (0.0745, 0.2941, 0.7294)]
            print(f"  Mandiri Credit Green (#06AA6F) glyphs: {len(green_chars)}")
            print(f"  Mandiri Saldo Blue   (#134BBA) glyphs: {len(blue_chars)}")
            print()


def main():
    parser = argparse.ArgumentParser(description="PDFCraft Copilot CLI")
    parser.add_argument("--excel", help="Path to input Excel mutasi bank template")
    parser.add_argument("--repair", help="Path to faulty PDF statement to repair")
    parser.add_argument("--audit", help="Path to PDF statement to audit")
    parser.add_argument("--output", help="Path for output PDF statement")

    args = parser.parse_args()

    if args.audit:
        run_audit(args.audit)
    elif args.repair:
        if not args.output:
            args.output = os.path.join(
                os.path.dirname(__file__), "..", "output", "REPAIRED_STATEMENT.pdf"
            )
        doctor = StatementDoctor()
        doctor.repair_statement(args.repair, args.output)
        run_audit(args.output)
    elif args.excel:
        if not args.output:
            args.output = os.path.join(
                os.path.dirname(__file__), "..", "output", "STANDARDIZED_STATEMENT.pdf"
            )
        builder = StatementBuilder()
        builder.build_from_excel(args.excel, args.output)
        run_audit(args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
