"""
Bank Mandiri e-Statement Ground Truth Specification
Defines exact geometric coordinates, color palettes, and layout rules derived from
authentic reference documents (Agu 2026, Mei 2026, Des 2024).
"""

from dataclasses import dataclass
from typing import Tuple

# --- PAGE DIMENSIONS (A4 Portrait) ---
PAGE_WIDTH = 595.00
PAGE_HEIGHT = 842.00

# --- VERTICAL GRID INTERVAL ---
ROW_HEIGHT_DELTA_Y = 46.00  # Constant vertical delta between transaction rows

# --- PAGE 1 GRID GEOMETRY ---
PAGE_1_MAX_ROWS = 10
PAGE_1_ROW_1_BASE_Y = 343.92  # Baseline of first transaction on Page 1

# --- INTERMEDIATE PAGE GRID GEOMETRY ---
PAGE_N_MAX_ROWS = 12
PAGE_N_ROW_1_BASE_Y = 227.92  # Baseline of first transaction on Page 2..N

# ==============================================================================
# RATA KIRI (LEFT-ALIGNED SHARED X0 ANCHORS)
# ==============================================================================
# Margin 16.00 pt: Primary left boundary for header labels & products
ANCHOR_LEFT_MARGIN_X0 = 16.00    # 'e-Statement', 'Nama/Name', 'Cabang/Branch', 'Tabungan NOW IDR', 'Nomor Rekening/Account Number', 'Mata Uang/Currency'
LABEL_COL1_X0 = 16.00

# Table Columns (Left-aligned)
COL_NO_X = 20.00                 # 'No' column header and row indices (1, 2, 3...)
COL_NO_X0 = 20.00
COL_DATE_X = 52.00               # 'Tanggal / Date' header, transaction date ('DD Mon YYYY')
COL_DATE_TIME_X0 = 52.00
COL_TIME_X = 52.00               # Transaction time ('HH:MM:SS WIB')
COL_DESC_X = 124.00              # 'Keterangan / Remarks' header, all transaction description lines
COL_DESC_X0 = 124.00

# Metadata Columns & Colons (Left-aligned)
COLON_COL1_X0 = 111.00           # ':' colon for 'Nama' and 'Cabang'
VALUE_COL1_X0 = 123.00           # Customer Name ('GALANG...', 'ROY...'), Branch ('KCP Serang Ciruas', 'KCP Jakarta...')
CUSTOMER_NAME_X = 123.00
CUSTOMER_NAME_Y = 99.92
CUSTOMER_NAME_MAX_WIDTH = 120.00 # Wrapping width for names

BRANCH_X = 123.00
BRANCH_Y = 121.92

COLON_ACC_X0 = 148.00            # ':' colon for 'Nomor Rekening' and 'Mata Uang'
VALUE_ACC_X0 = 160.00            # Account Number ('16300...'), Currency ('IDR')
ACCOUNT_NUMBER_LABEL_X = 16.00
ACCOUNT_NUMBER_VALUE_X = 160.00
ACCOUNT_NUMBER_Y = 188.92

CURRENCY_VALUE_X = 160.00
CURRENCY_Y = 210.92

LABEL_COL2_X0 = 233.00           # 'Periode/Period', 'Dicetak pada/Issued on'
PERIOD_LABEL_X = 233.00
PERIOD_Y = 99.92
PRINT_DATE_LABEL_X = 233.00
PRINT_DATE_Y = 121.92

COLON_COL2_X0 = 326.00           # ':' colon for 'Periode' and 'Dicetak pada'
VALUE_COL2_X0 = 340.00           # Periode range ('01 Jul 2026 - 31 Jul 2026'), Print Date ('19 Oct 2026')
PERIOD_VALUE_X = 340.00
PRINT_DATE_VALUE_X = 340.00

# Financial Summary Box (Left-aligned labels & colons)
SUMMARY_LABEL_X0 = 298.00        # 'Saldo Awal/Initial Balance', 'Dana Masuk/...', 'Dana Keluar/...', 'Saldo Akhir/...'
SUMMARY_COLON_X0 = 446.12        # ':' colons for financial summary box
SUMMARY_COLON_X1 = 447.88

SUMMARY_SALDO_AWAL_Y = 168.92
SUMMARY_DANA_MASUK_Y = 191.92
SUMMARY_DANA_KELUAR_Y = 214.92
SUMMARY_SALDO_AKHIR_Y = 238.92

# ==============================================================================
# RATA KANAN (RIGHT-ALIGNED SHARED X1 ANCHORS)
# ==============================================================================
# Table Nominal (Strict Right Edge = 432.00 pt)
COL_NOMINAL_RIGHT_X = 432.00     # Backwards-compatible alias
COL_NOMINAL_RIGHT_X1 = 432.00    # Header 'Nominal (IDR)' / 'Amount (IDR)', ALL transaction amounts ('+xxx.xxx,xx' / '-xxx.xxx,xx')

# Table Running Saldo (Strict Right Edge = 571.00 pt)
COL_SALDO_RIGHT_X = 571.00       # Backwards-compatible alias
COL_SALDO_RIGHT_X1 = 571.00      # Header 'Saldo (IDR)' / 'Balance (IDR)', ALL transaction running saldos ('xxx.xxx,xx')

# Financial Summary Box (Strict Right Edge = 567.00 pt)
SUMMARY_RIGHT_X = 567.00         # Backwards-compatible alias
SUMMARY_VALUE_RIGHT_X1 = 567.00  # ALL 4 financial summary values ('Saldo Awal', 'Dana Masuk', 'Dana Keluar', 'Saldo Akhir')

# Document Boundaries & Footers (Strict Right Edge = 579.00 pt)
HEADER_ADDRESS_RIGHT_X1 = 579.00 # Bank Address '... Indonesia'
FOOTER_CALL_RIGHT_X1 = 579.00    # 'Mandiri Call 14000'

# Bilingual Page Number Anchors
PAGE_NUM_RIGHT_X = 563.96        # Backwards-compatible alias
PAGE_NUM_RIGHT_X1 = 563.96       # Maximum right boundary for 'X dari Y' (563.96) and 'X of Y' (563.16)
PAGE_NUM_DARI_OF_RIGHT_X1 = 554.00 # Shared right edge of 'dari' and 'of'
PAGE_NUM_ID_Y = 99.92            # "X dari Y"
PAGE_NUM_EN_Y = 109.92           # "X of Y"

# --- COLOR PALETTES (Exact Hex Strings) ---
COLOR_CREDIT_GREEN = "#06AA6F"         # Incoming transactions (+)
COLOR_RUNNING_SALDO_BLUE = "#134BBA"   # Running saldo & closing saldo
COLOR_DEBIT_BLACK = "#1A1A1A"          # Outgoing transactions (-)
COLOR_SALDO_AWAL_GRAY = "#615A5A"      # Initial balance
COLOR_REGULATORY_GRAY = "#ADA6AE"      # Border lines & OJK/BI/LPS regulatory footer
COLOR_TEXT_DARK = "#1A1A1A"            # Standard text
COLOR_HEADER_WHITE = "#FFFFFF"         # Banner white text

# --- DISCLAIMER FORMATS ---
# Format A: Inline disclaimer (when last page has <= 7 rows)
INLINE_DISCLAIMER_GAP_BATAS_Y = 38.00  # From last transaction base to "batas akhir transaksi"
INLINE_DISCLAIMER_GAP_BODY_Y = 90.00   # From last transaction base to disclaimer text

# Format B: Dedicated disclaimer spread (Mei 2026 Page 14 ground truth)
STANDALONE_BATAS_Y = 11.92
STANDALONE_TITLE_Y = 63.88
STANDALONE_BODY_START_Y = 88.92
STANDALONE_BODY_END_Y = 207.92
DISCLAIMER_HEADER_X0 = 32.00     # 'Disclaimer' header
DISCLAIMER_NUM_X0 = 32.00        # Item numbering '1.', '2.', '3.', '4.'
DISCLAIMER_BODY_X0 = 47.00       # Paragraph body for items 1-3 (48.00 for item 4)


def get_row_base_y(page_number: int, row_index: int) -> float:
    """
    Returns the exact theoretical Y baseline for row_index (1-based) on page_number (1-based).
    """
    if page_number == 1:
        if row_index > PAGE_1_MAX_ROWS:
            raise ValueError(f"Row index {row_index} exceeds Page 1 maximum ({PAGE_1_MAX_ROWS})")
        return PAGE_1_ROW_1_BASE_Y + (row_index - 1) * ROW_HEIGHT_DELTA_Y
    else:
        if row_index > PAGE_N_MAX_ROWS:
            raise ValueError(f"Row index {row_index} exceeds Page {page_number} maximum ({PAGE_N_MAX_ROWS})")
        return PAGE_N_ROW_1_BASE_Y + (row_index - 1) * ROW_HEIGHT_DELTA_Y


def format_nominal(amount: float, is_credit: bool) -> str:
    """Formats amount into Mandiri e-Statement format: +1.234.567,00 or -1.234.567,00."""
    prefix = "+" if is_credit else "-"
    formatted_num = f"{abs(amount):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{prefix}{formatted_num}"


def format_saldo(amount: float) -> str:
    """Formats saldo into Mandiri e-Statement format: 1.234.567,00 (no sign)."""
    return f"{abs(amount):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
