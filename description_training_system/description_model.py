"""
Description Model Engine
Inference engine that transforms raw transaction descriptions into canonical,
multi-line structures with precise spatial centering for Bank Mandiri e-Statements.
"""

from typing import Any, Dict, List, Optional, Tuple
from .syntax_rules import TransactionCategory, TransactionSyntaxRule

DESC_COL_MAX_WIDTH = 240.00  # pt (From X=124.00 to approx X=364.00)
ROW_PITCH = 46.00             # pt (Vertical step between rows)


class DescriptionModelEngine:
    """Trained model engine for parsing and formatting descriptions."""

    @classmethod
    def format(cls, raw_text: str) -> Dict[str, Any]:
        """
        Parses and formats raw description text according to authentic Bank Mandiri rules.
        Returns formatted text, line breakdown, line count, and spatial offsets.
        """
        if not raw_text or not raw_text.strip():
            return {
                "category": TransactionCategory.GENERAL_TRANSFER.value,
                "lines": [""],
                "formatted_text": "",
                "line_count": 1,
                "target_top_offset": 0.0,
                "max_width": DESC_COL_MAX_WIDTH,
                "is_safe": True
            }

        text = raw_text.strip()
        cat = TransactionSyntaxRule.identify_category(text)

        if cat == TransactionCategory.PAYROLL_CORPORATE:
            lines = TransactionSyntaxRule.format_payroll_corporate(text)
        elif cat == TransactionCategory.BI_FAST:
            lines = TransactionSyntaxRule.format_bi_fast(text)
        elif cat == TransactionCategory.MANDIRI_INHOUSE:
            lines = TransactionSyntaxRule.format_mandiri_inhouse(text)
        elif cat == TransactionCategory.ATM_WITHDRAWAL:
            lines = TransactionSyntaxRule.format_atm_withdrawal(text)
        elif cat == TransactionCategory.QRIS_PAYMENT:
            lines = TransactionSyntaxRule.format_qris_payment(text)
        elif cat == TransactionCategory.ECOMMERCE:
            lines = TransactionSyntaxRule.format_ecommerce(text)
        elif cat == TransactionCategory.EWALLET_BILLER:
            lines = TransactionSyntaxRule.format_ewallet_biller(text)
        elif cat == TransactionCategory.BANK_FEES_ADMIN:
            lines = TransactionSyntaxRule.format_bank_fees(text)
        else:
            # Fallback
            parts = [p.strip() for p in text.split("\n") if p.strip()]
            lines = parts if parts else [text]

        # Enforce max 4 lines
        if len(lines) > 4:
            lines = lines[:4]

        line_count = len(lines)
        formatted_text = "\n".join(lines)

        # Calculate vertical centering offset relative to row baseline
        # 1 line: centered on baseline (offset = 0)
        # 2 lines: line 1 at baseline - 5pt, line 2 at baseline + 5pt
        # 3 lines: line 1 at baseline - 10pt, line 2 at baseline, line 3 at baseline + 10pt
        # 4 lines: line 1 at baseline - 15pt, line 2 at baseline - 5pt, line 3 at baseline + 5pt, line 4 at baseline + 15pt
        if line_count == 1:
            target_top_offset = 0.00
            estimated_height = 8.00
        elif line_count == 2:
            target_top_offset = -5.00
            estimated_height = 18.00
        elif line_count == 3:
            target_top_offset = -10.00
            estimated_height = 28.00
        else:  # 4 lines
            target_top_offset = -15.00
            estimated_height = 38.00

        # Safety check: Row height is 46pt. Gap to adjacent rows must be >= 8pt.
        is_safe = estimated_height <= (ROW_PITCH - 7.00)

        return {
            "category": cat.value,
            "lines": lines,
            "formatted_text": formatted_text,
            "line_count": line_count,
            "target_top_offset": target_top_offset,
            "estimated_height": estimated_height,
            "max_width": DESC_COL_MAX_WIDTH,
            "is_safe": is_safe
        }

    @classmethod
    def calculate_pdf_dy(cls, current_rect_top: float, row_base_y: float, line_count: int) -> float:
        """
        Calculates the exact translative dy in PDF coordinate space.
        In PDF coordinate space, Y increases UPWARDS (towards the top of the page).
        Therefore: dy_pdf = current_screen_top - target_screen_top
        """
        if line_count == 1:
            target_top_y = row_base_y
        elif line_count == 2:
            target_top_y = row_base_y - 5.00
        elif line_count == 3:
            target_top_y = row_base_y - 10.00
        else:  # 4 lines
            target_top_y = row_base_y - 15.00

        return current_rect_top - target_top_y
