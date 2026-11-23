"""
PDFCraft Statement Builder
End-to-End Orchestrator for Bank Mandiri e-Statements adhering strictly to
SOP 7-Tahap and authentic reference telemetry.
"""

import os
import sys
import re
from typing import Any, Callable, Dict, List, Optional

from bank_mandiri_spec import (
    COL_NOMINAL_RIGHT_X,
    COL_SALDO_RIGHT_X,
    SUMMARY_RIGHT_X,
    COL_NO_X,
    COL_DATE_TIME_X0,
    COL_DESC_X,
    VALUE_COL1_X0,
    VALUE_COL2_X0,
    VALUE_ACC_X0,
    COLOR_CREDIT_GREEN,
    COLOR_RUNNING_SALDO_BLUE,
    COLOR_DEBIT_BLACK,
    COLOR_SALDO_AWAL_GRAY,
    PAGE_1_MAX_ROWS,
    PAGE_N_MAX_ROWS
)
from pdfcraft_client import PdfCraftClient
from parse_excel_template import parse_xara_excel_template
from smart_date_time_generator import enrich_transactions_dates_and_times
from description_layout_engine import (
    DescriptionLayoutEngine,
    format_customer_name,
    DESC_COL_MAX_WIDTH
)


def find_paragraph(
    client: PdfCraftClient,
    doc_id: int,
    page: int,
    x_range: tuple,
    y_range: tuple,
    predicate: Optional[Callable[[Dict[str, Any]], bool]] = None
) -> Optional[Dict[str, Any]]:
    """
    Finds a paragraph on the given page dynamically based on bounding box
    and an optional predicate filter. Avoids stale paragraph index issues.
    """
    paras = client.get_paragraphs(doc_id, page=page)
    for p in paras:
        r = p["rect"]
        if x_range[0] <= r[0] <= x_range[1] and y_range[0] <= r[1] <= y_range[1]:
            if predicate is None or predicate(p):
                return p
    return None


class StatementBuilder:
    """Orchestrates generation of pixel-perfect e-Statements using PdfCraft."""

    def __init__(self, templates_dir: Optional[str] = None):
        if templates_dir is None:
            templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))
        self.templates_dir = templates_dir
        self.p1_template = os.path.join(templates_dir, "master_page_1.pdf")
        self.p_mid_template = os.path.join(templates_dir, "master_page_intermediate.pdf")
        self.p_disc_inline = os.path.join(templates_dir, "master_page_disclaimer_inline.pdf")
        self.p_disc_standalone = os.path.join(templates_dir, "master_page_disclaimer_standalone.pdf")

    def build_from_excel(self, excel_path: str, output_pdf_path: str) -> str:
        """
        Parses Excel, processes business logic, and generates a standardized PDF e-Statement.
        """
        # 1. Parse Excel data
        data = parse_xara_excel_template(excel_path)
        transactions = data.get("transactions", [])
        header = data.get("header", {})
        summary = data.get("summary", {})

        # Auto-enrich dates, times, and sequential numbering
        periode_str = header.get("periode", "")
        transactions = enrich_transactions_dates_and_times(transactions, periode_str)

        total_tx = len(transactions)
        print(f"[Builder] Total transactions to process: {total_tx}")

        # 2. Determine Page Layout
        page_paths = [self.p1_template]
        if total_tx > PAGE_1_MAX_ROWS:
            remaining_tx = total_tx - PAGE_1_MAX_ROWS
            num_mid_pages = (remaining_tx + PAGE_N_MAX_ROWS - 1) // PAGE_N_MAX_ROWS
            for _ in range(num_mid_pages):
                page_paths.append(self.p_mid_template)
            
            # If the last transaction page has 12 rows, use standalone disclaimer
            last_page_tx_count = remaining_tx % PAGE_N_MAX_ROWS
            if last_page_tx_count == 0:
                page_paths.append(self.p_disc_standalone)
        else:
            if total_tx == PAGE_1_MAX_ROWS:
                page_paths.append(self.p_disc_standalone)

        total_pages = len(page_paths)
        print(f"[Builder] Assembling {total_pages}-page document structure...")

        # 3. Assemble document using doc_combine
        temp_combined = os.path.join(os.path.dirname(output_pdf_path), "temp_assembly.pdf")
        with PdfCraftClient() as client:
            client.call_tool("doc_combine", {
                "paths": page_paths,
                "out": temp_combined,
                "open": False
            })

            # Open assembled document for SOP 7-Tahap editing
            doc_id = client.doc_open(temp_combined)
            print(f"[Builder] Editing assembled statement (doc_id={doc_id})...")

            # --- TAHAP 1 to 5: Header, Customer, Account, Page Numbers across all pages ---
            self._apply_sop_header_and_summary(
                client=client,
                doc_id=doc_id,
                header=header,
                summary=summary,
                total_pages=total_pages
            )

            # --- TAHAP 6 & 7: Transactions ---
            self._apply_sop_transactions(
                client=client,
                doc_id=doc_id,
                transactions=transactions
            )

            # Save to final output
            client.doc_save(doc_id, path=output_pdf_path, full=True)
            client.doc_close(doc_id)

        # Cleanup temp assembly
        if os.path.exists(temp_combined):
            try:
                os.remove(temp_combined)
            except OSError:
                pass

        print(f"[Builder] Statement successfully generated at: {output_pdf_path}")
        return output_pdf_path

    def _apply_sop_header_and_summary(
        self,
        client: PdfCraftClient,
        doc_id: int,
        header: Dict[str, Any],
        summary: Dict[str, Any],
        total_pages: int
    ):
        """Applies Tahap 1-5 and Financial Summary across all pages with dynamic paragraph discovery."""
        customer_name_raw = header.get("nama", "").upper()
        formatted_name, _ = format_customer_name(customer_name_raw)
        is_multiline_name = "\n" in formatted_name

        cabang = header.get("cabang", "KCP Serang Ciruas")
        periode = header.get("periode", "")
        dicetak_pada = header.get("dicetak_pada", "")
        nomor_rekening = header.get("nomor_rekening", "")

        for page_idx in range(1, total_pages + 1):
            # 1. Customer Name and Cabang (Tahap 1)
            p_cabang = find_paragraph(client, doc_id, page_idx, (115, 135), (118, 132))
            p_name = find_paragraph(client, doc_id, page_idx, (115, 135), (95, 110))

            if is_multiline_name:
                # Authentic Bank Mandiri 3-line composite block (Name 2 lines + Cabang 1 line)
                if p_cabang:
                    client.edit_text(doc_id, page=page_idx, paragraph=p_cabang["paragraph"], text="")
                
                # Re-query p_name in case paragraph IDs shifted
                p_name = find_paragraph(client, doc_id, page_idx, (115, 135), (95, 110))
                if p_name:
                    combined_block = f"{formatted_name}\n{cabang}"
                    client.edit_text(
                        doc_id,
                        page=page_idx,
                        paragraph=p_name["paragraph"],
                        text=combined_block,
                        line_spacing=1.375
                    )
                    # Align left edge to VALUE_COL1_X0 (123.00)
                    up_p = find_paragraph(client, doc_id, page_idx, (115, 135), (95, 110))
                    if up_p and abs(up_p["rect"][0] - VALUE_COL1_X0) > 0.05:
                        client.edit_text(doc_id, page=page_idx, paragraph=up_p["paragraph"], dx=VALUE_COL1_X0 - up_p["rect"][0])
            else:
                # Single-line name
                if p_name:
                    client.edit_text(doc_id, page=page_idx, paragraph=p_name["paragraph"], text=customer_name_raw)
                    up_p = find_paragraph(client, doc_id, page_idx, (115, 135), (95, 110))
                    if up_p and abs(up_p["rect"][0] - VALUE_COL1_X0) > 0.05:
                        client.edit_text(doc_id, page=page_idx, paragraph=up_p["paragraph"], dx=VALUE_COL1_X0 - up_p["rect"][0])

                if p_cabang:
                    client.edit_text(doc_id, page=page_idx, paragraph=p_cabang["paragraph"], text=cabang)
                    up_p = find_paragraph(client, doc_id, page_idx, (115, 135), (118, 132))
                    if up_p and abs(up_p["rect"][0] - VALUE_COL1_X0) > 0.05:
                        client.edit_text(doc_id, page=page_idx, paragraph=up_p["paragraph"], dx=VALUE_COL1_X0 - up_p["rect"][0])

            # 2. Periode (Tahap 2)
            p_periode = find_paragraph(client, doc_id, page_idx, (330, 370), (95, 110))
            if p_periode:
                client.edit_text(doc_id, page=page_idx, paragraph=p_periode["paragraph"], text=periode)
                up_p = find_paragraph(client, doc_id, page_idx, (330, 370), (95, 110))
                if up_p and abs(up_p["rect"][0] - VALUE_COL2_X0) > 0.05:
                    client.edit_text(doc_id, page=page_idx, paragraph=up_p["paragraph"], dx=VALUE_COL2_X0 - up_p["rect"][0])

            # 3. Dicetak Pada (Tahap 3)
            p_dicetak = find_paragraph(client, doc_id, page_idx, (330, 370), (118, 132))
            if p_dicetak:
                client.edit_text(doc_id, page=page_idx, paragraph=p_dicetak["paragraph"], text=dicetak_pada)
                up_p = find_paragraph(client, doc_id, page_idx, (330, 370), (118, 132))
                if up_p and abs(up_p["rect"][0] - VALUE_COL2_X0) > 0.05:
                    client.edit_text(doc_id, page=page_idx, paragraph=up_p["paragraph"], dx=VALUE_COL2_X0 - up_p["rect"][0])

            # 4. Page Numbers (Tahap 5)
            # Find and clear orphaned digit if any
            p_orphan = find_paragraph(client, doc_id, page_idx, (545, 575), (90, 108), lambda p: p["text"].strip().isdigit())
            if p_orphan:
                client.edit_text(doc_id, page=page_idx, paragraph=p_orphan["paragraph"], text="")

            p_dari = find_paragraph(client, doc_id, page_idx, (520, 565), (90, 115), lambda p: "dari" in p["text"])
            if p_dari:
                client.edit_text(doc_id, page=page_idx, paragraph=p_dari["paragraph"], text=f"{page_idx} dari {total_pages}", width=50.0)

            p_of = find_paragraph(client, doc_id, page_idx, (530, 570), (105, 125), lambda p: "of" in p["text"])
            if p_of:
                client.edit_text(doc_id, page=page_idx, paragraph=p_of["paragraph"], text=f"{page_idx} of {total_pages}", width=50.0)

            # 5. Page 1 Specific: Account Number and Financial Summary
            if page_idx == 1:
                # Nomor Rekening (Tahap 4)
                p_acc = find_paragraph(client, doc_id, 1, (140, 185), (185, 202))
                if p_acc:
                    client.edit_text(doc_id, page=1, paragraph=p_acc["paragraph"], text=f"{nomor_rekening} ")
                    up_p = find_paragraph(client, doc_id, 1, (140, 185), (185, 202))
                    if up_p and abs(up_p["rect"][0] - VALUE_ACC_X0) > 0.05:
                        client.edit_text(doc_id, page=1, paragraph=up_p["paragraph"], dx=VALUE_ACC_X0 - up_p["rect"][0])

                # Financial Summary Box (Tahap 7)
                # Saldo Awal
                if "saldo_awal" in summary:
                    p_sawal = find_paragraph(client, doc_id, 1, (480, 585), (160, 180))
                    if p_sawal:
                        client.edit_text(doc_id, page=1, paragraph=p_sawal["paragraph"], text=summary["saldo_awal"], color=COLOR_SALDO_AWAL_GRAY)
                        up_p = find_paragraph(client, doc_id, 1, (480, 585), (160, 180))
                        if up_p:
                            dx = SUMMARY_RIGHT_X - up_p["rect"][2]
                            if abs(dx) > 0.01:
                                client.edit_text(doc_id, page=1, paragraph=up_p["paragraph"], dx=dx)

                # Dana Masuk
                if "dana_masuk" in summary:
                    p_dmasuk = find_paragraph(client, doc_id, 1, (480, 585), (185, 205))
                    if p_dmasuk:
                        client.edit_text(doc_id, page=1, paragraph=p_dmasuk["paragraph"], text=f"+ {summary['dana_masuk']}", color=COLOR_CREDIT_GREEN)
                        up_p = find_paragraph(client, doc_id, 1, (480, 585), (185, 205))
                        if up_p:
                            dx = SUMMARY_RIGHT_X - up_p["rect"][2]
                            if abs(dx) > 0.01:
                                client.edit_text(doc_id, page=1, paragraph=up_p["paragraph"], dx=dx)

                # Dana Keluar
                if "dana_keluar" in summary:
                    p_dkeluar = find_paragraph(client, doc_id, 1, (480, 585), (208, 228))
                    if p_dkeluar:
                        client.edit_text(doc_id, page=1, paragraph=p_dkeluar["paragraph"], text=f"- {summary['dana_keluar']}", color=COLOR_DEBIT_BLACK)
                        up_p = find_paragraph(client, doc_id, 1, (480, 585), (208, 228))
                        if up_p:
                            dx = SUMMARY_RIGHT_X - up_p["rect"][2]
                            if abs(dx) > 0.01:
                                client.edit_text(doc_id, page=1, paragraph=up_p["paragraph"], dx=dx)

                # Saldo Akhir
                if "saldo_akhir" in summary:
                    p_sakhir = find_paragraph(client, doc_id, 1, (480, 585), (230, 255))
                    if p_sakhir:
                        client.edit_text(doc_id, page=1, paragraph=p_sakhir["paragraph"], text=summary["saldo_akhir"], color=COLOR_RUNNING_SALDO_BLUE)
                        up_p = find_paragraph(client, doc_id, 1, (480, 585), (230, 255))
                        if up_p:
                            dx = SUMMARY_RIGHT_X - up_p["rect"][2]
                            if abs(dx) > 0.01:
                                client.edit_text(doc_id, page=1, paragraph=up_p["paragraph"], dx=dx)

    def _apply_sop_transactions(
        self,
        client: PdfCraftClient,
        doc_id: int,
        transactions: List[Dict[str, Any]]
    ):
        """Populates transactions row by row across Page 1 and subsequent pages."""
        tx_idx = 0
        total_tx = len(transactions)
        page_num = 1

        while tx_idx < total_tx:
            max_rows = PAGE_1_MAX_ROWS if page_num == 1 else PAGE_N_MAX_ROWS
            page_txs = transactions[tx_idx : tx_idx + max_rows]
            
            self._populate_page_transactions(client, doc_id, page=page_num, page_txs=page_txs)
            
            tx_idx += len(page_txs)
            page_num += 1

    def _populate_page_transactions(
        self,
        client: PdfCraftClient,
        doc_id: int,
        page: int,
        page_txs: List[Dict[str, Any]]
    ):
        """Populates transactions for a single page with dynamic discovery and strict anchor alignments."""
        base_y_start = 343.92 if page == 1 else 227.92
        max_rows = PAGE_1_MAX_ROWS if page == 1 else PAGE_N_MAX_ROWS

        for r_i, tx in enumerate(page_txs):
            row_y = base_y_start + r_i * 46.00

            # 1. No -> Left anchor = COL_NO_X (20.00)
            p_no = find_paragraph(client, doc_id, page, (15, 35), (row_y - 15, row_y + 15), lambda p: p["text"].strip().isdigit())
            if p_no:
                client.edit_text(doc_id, page=page, paragraph=p_no["paragraph"], text=str(tx["no"]))
                up_p = find_paragraph(client, doc_id, page, (15, 35), (row_y - 15, row_y + 15), lambda p: p["text"].strip().isdigit())
                if up_p and abs(up_p["rect"][0] - COL_NO_X) > 0.05:
                    client.edit_text(doc_id, page=page, paragraph=up_p["paragraph"], dx=COL_NO_X - up_p["rect"][0])

            # 2. Tanggal -> Left anchor = COL_DATE_TIME_X0 (52.00)
            p_date = find_paragraph(client, doc_id, page, (45, 75), (row_y - 15, row_y + 5))
            if p_date:
                date_val = tx.get("tanggal_full", tx.get("tanggal", ""))
                client.edit_text(doc_id, page=page, paragraph=p_date["paragraph"], text=date_val)
                up_p = find_paragraph(client, doc_id, page, (45, 75), (row_y - 15, row_y + 5))
                if up_p and abs(up_p["rect"][0] - COL_DATE_TIME_X0) > 0.05:
                    client.edit_text(doc_id, page=page, paragraph=up_p["paragraph"], dx=COL_DATE_TIME_X0 - up_p["rect"][0])

            # 3. Jam -> Left anchor = COL_DATE_TIME_X0 (52.00)
            p_time = find_paragraph(client, doc_id, page, (45, 75), (row_y + 2, row_y + 20))
            if p_time:
                client.edit_text(doc_id, page=page, paragraph=p_time["paragraph"], text=tx["jam"])
                up_p = find_paragraph(client, doc_id, page, (45, 75), (row_y + 2, row_y + 20))
                if up_p and abs(up_p["rect"][0] - COL_DATE_TIME_X0) > 0.05:
                    client.edit_text(doc_id, page=page, paragraph=up_p["paragraph"], dx=COL_DATE_TIME_X0 - up_p["rect"][0])

            # 4. Keterangan -> Left anchor = COL_DESC_X (124.00) with vertical centering
            p_desc = find_paragraph(client, doc_id, page, (120, 135), (row_y - 20, row_y + 20))
            if p_desc:
                raw_desc = str(tx.get("uraian", "") or "").strip()
                if not raw_desc:
                    client.edit_text(doc_id, page=page, paragraph=p_desc["paragraph"], text="")
                else:
                    desc_val = DescriptionLayoutEngine.format_description(raw_desc)
                    line_count = len(desc_val.split("\n"))

                    if line_count == 1:
                        target_top_y = row_y
                    elif line_count == 2:
                        target_top_y = row_y - 5.00
                    elif line_count == 3:
                        target_top_y = row_y - 10.00
                    else:  # 4 lines (e.g. Corporate Payroll / BI Fast with remark)
                        target_top_y = row_y - 15.00

                    # In PDF coordinate space, moving UP requires POSITIVE dy: dy_pdf = current_top_y - target_top_y
                    dy = p_desc["rect"][1] - target_top_y

                    client.edit_text(
                        doc_id,
                        page=page,
                        paragraph=p_desc["paragraph"],
                        text=desc_val,
                        width=DESC_COL_MAX_WIDTH,
                        dy=dy if abs(dy) >= 0.5 else None
                    )
                    up_p = find_paragraph(client, doc_id, page, (120, 135), (row_y - 20, row_y + 20))
                    if up_p and abs(up_p["rect"][0] - COL_DESC_X) > 0.05:
                        client.edit_text(doc_id, page=page, paragraph=up_p["paragraph"], dx=COL_DESC_X - up_p["rect"][0])

            # 5. Nominal -> Right anchor = COL_NOMINAL_RIGHT_X (432.00)
            p_nom = find_paragraph(client, doc_id, page, (370, 450), (row_y - 15, row_y + 15))
            if p_nom:
                nom_val = str(tx.get("nominal", "")).strip()
                is_credit = tx.get("tipe") == "CR" or nom_val.startswith("+")
                if is_credit and not nom_val.startswith("+"):
                    nom_val = f"+{nom_val}"
                elif not is_credit and not nom_val.startswith("-"):
                    nom_val = f"-{nom_val}"
                color = COLOR_CREDIT_GREEN if is_credit else COLOR_DEBIT_BLACK

                client.edit_text(doc_id, page=page, paragraph=p_nom["paragraph"], text=nom_val, color=color)
                up_p = find_paragraph(client, doc_id, page, (370, 450), (row_y - 15, row_y + 15))
                if up_p:
                    dx = COL_NOMINAL_RIGHT_X - up_p["rect"][2]
                    if abs(dx) > 0.01:
                        client.edit_text(doc_id, page=page, paragraph=up_p["paragraph"], dx=dx)

            # 6. Saldo -> Right anchor = COL_SALDO_RIGHT_X (571.00)
            p_sal = find_paragraph(client, doc_id, page, (490, 585), (row_y - 15, row_y + 15))
            if p_sal:
                saldo_val = str(tx.get("saldo", "")).strip()
                client.edit_text(doc_id, page=page, paragraph=p_sal["paragraph"], text=saldo_val, color=COLOR_RUNNING_SALDO_BLUE)
                up_p = find_paragraph(client, doc_id, page, (490, 585), (row_y - 15, row_y + 15))
                if up_p:
                    dx = COL_SALDO_RIGHT_X - up_p["rect"][2]
                    if abs(dx) > 0.01:
                        client.edit_text(doc_id, page=page, paragraph=up_p["paragraph"], dx=dx)

        # Blank out unused rows on the last page if fewer than max_rows
        if len(page_txs) < max_rows:
            for unused_r_i in range(len(page_txs), max_rows):
                unused_y = base_y_start + unused_r_i * 46.00
                paras = client.get_paragraphs(doc_id, page=page)
                for p in paras:
                    if abs(p["rect"][1] - unused_y) < 20.0 and p["rect"][1] >= 200:
                        client.edit_text(doc_id, page=page, paragraph=p["paragraph"], text="")
