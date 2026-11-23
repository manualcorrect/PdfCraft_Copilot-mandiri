"""
PDFCraft Statement Doctor & Auditor
Detects and repairs layout misalignments, color anomalies, and split text runs
in existing Bank Mandiri e-Statements using PdfCraft.
"""

import os
import sys
import re
import shutil
from typing import Any, Dict, List, Optional, Tuple

from bank_mandiri_spec import (
    COL_NOMINAL_RIGHT_X,
    COL_SALDO_RIGHT_X,
    SUMMARY_RIGHT_X,
    COLOR_CREDIT_GREEN,
    COLOR_RUNNING_SALDO_BLUE,
    COLOR_DEBIT_BLACK,
    COLOR_SALDO_AWAL_GRAY,
    PAGE_NUM_RIGHT_X
)
from pdfcraft_client import PdfCraftClient
from pdfcraft_editor import PdfCraftEditor


class StatementDoctor:
    """Audits and repairs bank statements to meet reference standards."""

    def __init__(self):
        pass

    def repair_statement(self, input_pdf: str, output_pdf: str) -> Dict[str, Any]:
        """
        Runs comprehensive auto-repair on input_pdf and saves standardized output to output_pdf.
        """
        # Copy input to output first so original is never touched
        os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
        shutil.copyfile(input_pdf, output_pdf)

        audit_log = {
            "financial_summary_fixed": 0,
            "nominal_alignments_fixed": 0,
            "saldo_alignments_fixed": 0,
            "split_runs_merged": 0,
            "page_numbers_fixed": 0
        }

        with PdfCraftClient() as client:
            editor = PdfCraftEditor(client)
            doc_id = client.doc_open(output_pdf)
            info = client.doc_info(doc_id)
            total_pages = len(info.get("pages", []))

            print(f"[Doctor] Diagnosing {input_pdf} ({total_pages} pages)...")

            # 1. Page 1: Repair Financial Summary Box
            summary_res = editor.fix_financial_summary(doc_id, page=1)
            audit_log["financial_summary_fixed"] += len(summary_res)

            # 2. Repair each page: Table Alignments, Colors, and Split Runs
            for page_idx in range(1, total_pages + 1):
                # A. Fix transaction table items
                table_res = editor.fix_transaction_table(doc_id, page=page_idx)
                for item in table_res:
                    if item["type"] == "Nominal":
                        audit_log["nominal_alignments_fixed"] += 1
                    elif item["type"] == "Saldo":
                        audit_log["saldo_alignments_fixed"] += 1

                # B. Merge split runs on this page
                split_count = self._repair_split_runs(client, doc_id, page=page_idx)
                audit_log["split_runs_merged"] += split_count

                # C. Ensure bilingual page numbering
                editor.fix_page_numbers(doc_id, page=page_idx, current_page=page_idx, total_pages=total_pages)
                audit_log["page_numbers_fixed"] += 1

            # Save and close
            client.doc_save(doc_id, full=True)
            client.doc_close(doc_id)

        print(f"[Doctor] Repair complete. Saved to: {output_pdf}")
        print(f"[Doctor] Audit Summary: {audit_log}")
        return audit_log

    def _repair_split_runs(self, client: PdfCraftClient, doc_id: int, page: int) -> int:
        """
        Identifies and merges split runs (e.g. split time '09' + ':49:44 WIB' or broken words).
        """
        paras = client.get_paragraphs(doc_id, page=page)
        merged_count = 0

        # Scan for time split runs at X ~ 52
        time_fragments = []
        for p in paras:
            txt = p["text"].strip()
            rect = p["rect"]
            if 45 <= rect[0] <= 80 and 320 <= rect[1] <= 800:
                if re.match(r"^\d{1,2}$", txt):
                    time_fragments.append((p, "hour"))
                elif txt.startswith(":") and "WIB" in txt:
                    time_fragments.append((p, "rest"))

        # Pair adjacent hour + rest fragments with similar Y coordinate
        for h_p, h_type in time_fragments:
            if h_type != "hour":
                continue
            for r_p, r_type in time_fragments:
                if r_type != "rest":
                    continue
                if abs(h_p["rect"][1] - r_p["rect"][1]) < 3.0:
                    # Found split time pair!
                    combined_time = f"{h_p['text'].strip()}{r_p['text'].strip()}"
                    # Edit the hour paragraph to contain the full time
                    client.edit_text(doc_id, page=page, paragraph=h_p["paragraph"], text=combined_time)
                    # Blank out the rest paragraph
                    client.edit_text(doc_id, page=page, paragraph=r_p["paragraph"], text="")
                    merged_count += 1

        return merged_count
