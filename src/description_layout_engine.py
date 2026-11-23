"""
Description Layout Engine
Wrapper providing backward compatibility and integration between
PdfCraft Statement Builder and the Description Training System.
"""

import os
import sys
from typing import Dict, List, Optional, Tuple

# Ensure Description Training System can be imported
SYS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SYS_ROOT not in sys.path:
    sys.path.append(SYS_ROOT)

from description_training_system.description_model import DescriptionModelEngine, DESC_COL_MAX_WIDTH, ROW_PITCH

DESC_COL_LEFT_X = 124.00
DESC_LINE_SPACING = 10.00


def format_customer_name(name: str) -> Tuple[str, Optional[float]]:
    """
    Splits long customer names (> 20 characters) into 2 lines adhering to
    Galang original e-Statement layout, keeping line 1 and line 2 starting at X0=123.00 pt.
    Returns (formatted_text, line_spacing).
    """
    clean_name = name.strip().upper()
    if len(clean_name) <= 20:
        return clean_name, None

    words = clean_name.split()
    if len(words) < 2:
        return clean_name, None

    if len(words) == 3:
        line1 = f"{words[0]} {words[1]}"
        line2 = words[2]
    elif len(words) == 2:
        line1 = words[0]
        line2 = words[1]
    else:
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])

    return f"{line1}\n{line2}", 1.375


class DescriptionLayoutEngine:
    """Delegates parsing, formatting, and vertical metrics to DescriptionModelEngine."""

    @staticmethod
    def format_description(raw_desc: str) -> str:
        """Formats raw description text into canonical multi-line layout."""
        model_result = DescriptionModelEngine.format(raw_desc)
        return model_result["formatted_text"]

    @staticmethod
    def get_details(raw_desc: str) -> Dict[str, any]:
        """Returns full parsing metadata including lines, count, and target vertical offset."""
        return DescriptionModelEngine.format(raw_desc)

    @staticmethod
    def calculate_dy(current_rect_top: float, row_base_y: float, line_count: int) -> float:
        """Calculates translation dy in PDF coordinate space."""
        return DescriptionModelEngine.calculate_pdf_dy(current_rect_top, row_base_y, line_count)
