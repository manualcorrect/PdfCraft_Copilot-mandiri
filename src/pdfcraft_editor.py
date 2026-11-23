"""
PdfCraft Editor Engine
High-level PDF editing and standardization logic built on top of PdfCraftClient.
Enforces Bank Mandiri geometric and color specifications.
"""

import re
from typing import Any, Dict, List, Optional, Tuple
from bank_mandiri_spec import (
    COL_NOMINAL_RIGHT_X,
    COL_SALDO_RIGHT_X,
    SUMMARY_RIGHT_X,
    COL_NO_X,
    COL_DATE_TIME_X0,
    COL_DESC_X,
    COLOR_CREDIT_GREEN,
    COLOR_RUNNING_SALDO_BLUE,
    COLOR_DEBIT_BLACK,
    COLOR_SALDO_AWAL_GRAY,
    PAGE_NUM_RIGHT_X
)
from pdfcraft_client import PdfCraftClient


class PdfCraftEditor:
    """Provides high-level banking document editing operations."""

    def __init__(self, client: PdfCraftClient):
        self.client = client

    def right_align(
        self,
        doc_id: int,
        page: int,
        para: Dict[str, Any],
        target_x1: float,
        color: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Shifts a paragraph so its right edge (rect[2]) aligns exactly with target_x1.
        """
        current_x1 = para["rect"][2]
        dx = target_x1 - current_x1
        if abs(dx) < 0.01 and color is None:
            return {}
        return self.client.edit_text(
            doc_id=doc_id,
            page=page,
            paragraph=para["paragraph"],
            dx=dx if abs(dx) >= 0.01 else None,
            color=color
        )

    def fix_financial_summary(self, doc_id: int, page: int = 1) -> List[Dict[str, Any]]:
        """
        Standardizes the 4 financial summary values (Saldo Awal, Dana Masuk, Dana Keluar, Saldo Akhir)
        on Page 1 to SUMMARY_RIGHT_X (567.00 pt) with standard color palettes.
        """
        paras = self.client.get_paragraphs(doc_id, page=page)
        results = []

        for p in paras:
            rect = p["rect"]
            text = p["text"].strip()
            # Summary numbers are located at X > 480 and Y between 160 and 255
            if rect[0] > 480 and 160 <= rect[1] <= 255:
                # 1. Saldo Awal (approx Y=168)
                if 160 <= rect[1] <= 180:
                    res = self.right_align(doc_id, page, p, SUMMARY_RIGHT_X, COLOR_SALDO_AWAL_GRAY)
                    results.append({"type": "Saldo Awal", "res": res})
                # 2. Dana Masuk (approx Y=191, starts with +)
                elif 185 <= rect[1] <= 205:
                    res = self.right_align(doc_id, page, p, SUMMARY_RIGHT_X, COLOR_CREDIT_GREEN)
                    results.append({"type": "Dana Masuk", "res": res})
                # 3. Dana Keluar (approx Y=214, starts with -)
                elif 208 <= rect[1] <= 228:
                    res = self.right_align(doc_id, page, p, SUMMARY_RIGHT_X, COLOR_DEBIT_BLACK)
                    results.append({"type": "Dana Keluar", "res": res})
                # 4. Saldo Akhir (approx Y=238)
                elif 230 <= rect[1] <= 255:
                    res = self.right_align(doc_id, page, p, SUMMARY_RIGHT_X, COLOR_RUNNING_SALDO_BLUE)
                    results.append({"type": "Saldo Akhir", "res": res})

        return results

    def fix_transaction_table(self, doc_id: int, page: int) -> List[Dict[str, Any]]:
        """
        Standardizes all nominal amounts and running saldos on the given page:
        - Nominal Right Edge -> COL_NOMINAL_RIGHT_X (432.00 pt)
        - Nominal Credit Color -> COLOR_CREDIT_GREEN (#06AA6F)
        - Nominal Debit Color -> COLOR_DEBIT_BLACK (#1A1A1A)
        - Saldo Right Edge -> COL_SALDO_RIGHT_X (571.00 pt)
        - Saldo Color -> COLOR_RUNNING_SALDO_BLUE (#134BBA)
        """
        paras = self.client.get_paragraphs(doc_id, page=page)
        results = []

        for p in paras:
            rect = p["rect"]
            text = p["text"].strip()

            # Skip table header rows (Y < 320 on Page 1, Y < 210 on Page 2+)
            min_y = 320 if page == 1 else 200
            if rect[1] < min_y or rect[3] > 800:
                continue

            # Check for Nominal (approx X in [370..450], formatted currency)
            if 370 <= rect[0] <= 450 and (
                text.startswith("+") or text.startswith("-") or re.search(r"^\d{1,3}(\.\d{3})*,\d{2}$", text)
            ):
                is_credit = text.startswith("+")
                color = COLOR_CREDIT_GREEN if is_credit else COLOR_DEBIT_BLACK
                res = self.right_align(doc_id, page, p, COL_NOMINAL_RIGHT_X, color)
                results.append({"type": "Nominal", "text": text, "res": res})

            # Check for Running Saldo (approx X in [490..585], format xxx.xxx,xx without leading +/-)
            elif 490 <= rect[0] <= 585 and re.match(r"^\d{1,3}(\.\d{3})*,\d{2}$", text):
                res = self.right_align(doc_id, page, p, COL_SALDO_RIGHT_X, COLOR_RUNNING_SALDO_BLUE)
                results.append({"type": "Saldo", "text": text, "res": res})

        return results

    def fix_page_numbers(self, doc_id: int, page: int, current_page: int, total_pages: int):
        """
        Standardizes bilingual page numbering on top-right:
        'X dari Y' (Bold) and 'X of Y' (Italic).
        """
        paras = self.client.get_paragraphs(doc_id, page=page)
        for p in paras:
            rect = p["rect"]
            text = p["text"].strip()
            if 500 <= rect[0] <= 580 and 90 <= rect[1] <= 130:
                if "dari" in text:
                    new_text = f"{current_page} dari {total_pages}"
                    self.client.edit_text(doc_id, page, paragraph=p["paragraph"], text=new_text, width=50.0)
                elif "of" in text:
                    new_text = f"{current_page} of {total_pages}"
                    self.client.edit_text(doc_id, page, paragraph=p["paragraph"], text=new_text, width=50.0)
                elif text.isdigit() and rect[1] < 105:
                    self.client.edit_text(doc_id, page, paragraph=p["paragraph"], text="")
