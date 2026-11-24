"""
Transaction Syntax Rules & Grammar Models
Formal grammars and pattern recognizers extracted from authentic Bank Mandiri statements.
"""

import re
from enum import Enum
from typing import Dict, List, Optional, Tuple


class TransactionCategory(Enum):
    PAYROLL_CORPORATE = "PAYROLL_CORPORATE"
    BI_FAST = "BI_FAST"
    MANDIRI_INHOUSE = "MANDIRI_INHOUSE"
    ATM_WITHDRAWAL = "ATM_WITHDRAWAL"
    QRIS_PAYMENT = "QRIS_PAYMENT"
    ECOMMERCE = "ECOMMERCE"
    EWALLET_BILLER = "EWALLET_BILLER"
    BANK_FEES_ADMIN = "BANK_FEES_ADMIN"
    GENERAL_TRANSFER = "GENERAL_TRANSFER"


class TransactionSyntaxRule:
    """Encapsulates parsing, formatting, and vertical calculation rules for descriptions."""

    @staticmethod
    def identify_category(text: str) -> TransactionCategory:
        """Determines the appropriate category for a raw description text."""
        clean = " ".join(text.split())

        if "PT BENDI NASHA NIAGA INDUSTRI" in clean or "GAJI" in clean.upper() or "UPAH" in clean.upper():
            return TransactionCategory.PAYROLL_CORPORATE

        if re.search(r"Transfer\s+BI\s*Fast", clean, re.IGNORECASE):
            return TransactionCategory.BI_FAST

        if re.search(r"Transfer\s+(dari|ke|antar)\s+(?:BANK\s+)?MANDIRI", clean, re.IGNORECASE):
            return TransactionCategory.MANDIRI_INHOUSE

        if "Penarikan tunai" in clean:
            return TransactionCategory.ATM_WITHDRAWAL

        if "Pembayaran QR" in clean:
            return TransactionCategory.QRIS_PAYMENT

        if any(p in clean for p in ["Shopee Indonesia", "Tokopedia", "TikTok", "Blibli", "Lazada"]):
            return TransactionCategory.ECOMMERCE

        if any(clean.startswith(f) for f in ["Biaya", "Bunga", "Pajak", "BIAYA", "BUNGA", "PAJAK"]):
            return TransactionCategory.BANK_FEES_ADMIN

        if any(p in clean for p in ["Danatopup", "Instamoney", "Top-up e-money", "Gopay", "OVO", "DANA", "Telkomsel", "PLN"]):
            return TransactionCategory.EWALLET_BILLER

        return TransactionCategory.GENERAL_TRANSFER

    @staticmethod
    def format_payroll_corporate(text: str) -> List[str]:
        """
        Formats Corporate Payroll transactions strictly adhering to authentic references
        (e.g., Salman REK APR26 Page 2 Row 4).
        Standard 4-line structure:
          Line 1: Transfer BI Fast (or Transfer BI FAST)
          Line 2: Dari BCA (or Dari [BANK])
          Line 3: PT BENDI NASHA NIAGA INDUSTRI 5411078192
          Line 4: (CENAIDJA) (or remark)
        """
        clean = " ".join(text.split())

        # Match Transfer BI Fast + Bank
        header_m = re.search(r"(Transfer\s+BI\s+Fast|Transfer\s+BI\s+FAST)\s+(Dari\s+[A-Za-z0-9]+|DARI\s+[A-Za-z0-9]+)", clean, re.IGNORECASE)
        line1 = "Transfer BI Fast"
        line2 = "Dari BCA"
        remaining = clean

        if header_m:
            line1 = header_m.group(1).strip()
            line2 = header_m.group(2).strip()
            # Title case normalization matching reference
            if line2.lower() == "dari bca":
                line2 = "Dari BCA"
            elif line2.lower() == "dari bri":
                line2 = "Dari BRI"
            remaining = clean[header_m.end():].strip()

        # Extract remark in parentheses e.g. (CENAIDJA)
        remark_m = re.search(r"(\([A-Za-z0-9]+\)|\bCICIL[^\n]*|\bUPAH[^\n]*|\bPELUNASAN[^\n]*|\bREIMBURSE[^\n]*|-)$", remaining)
        remark = ""
        if remark_m:
            remark = remark_m.group(1).strip()
            remaining = remaining[:remark_m.start()].strip()

        line3 = remaining.strip()
        if not line3:
            line3 = "PT BENDI NASHA NIAGA INDUSTRI 5411078192"

        lines = [line1, line2, line3]
        if remark:
            lines.append(remark)
        return lines

    @staticmethod
    def format_bi_fast(text: str) -> List[str]:
        """
        Formats BI Fast transactions:
          Line 1: Transfer BI Fast (or Transfer BI FAST)
          Line 2: Dari/Ke [BANK_NAME]
          Line 3: [NAME] [ACCOUNT_NUMBER]
          Line 4 (Optional): [REMARK]
        """
        clean = " ".join(text.split())

        # Header match: Transfer BI Fast (or FAST) + Dari/Ke [BANK]
        m = re.search(r"(Transfer\s+BI\s+Fast|Transfer\s+BI\s+FAST)\s+((?:Dari|Ke|DARI|KE)\s+[^0-9]+?)(?=\s+[A-Z0-9\s]{4,}|\s+\d{6,}|$)", clean, re.IGNORECASE)
        if m:
            line1 = m.group(1).strip()
            line2 = m.group(2).strip()
            rest = clean[m.end():].strip()

            # Separate remark if at end
            remark_m = re.search(r"(\bCICIL[^\n]*|\bUPAH[^\n]*|\bPELUNASAN[^\n]*|\bREIMBURSE[^\n]*|\bAsuransi[^\n]*|\bKekurangan[^\n]*|\bP\b|-|\([A-Za-z0-9]+\))$", rest, re.IGNORECASE)
            remark = ""
            if remark_m and len(rest[:remark_m.start()].strip()) > 3:
                remark = remark_m.group(1).strip()
                line3 = rest[:remark_m.start()].strip()
            else:
                line3 = rest

            lines = [line1, line2, line3]
            if remark:
                lines.append(remark)
            return lines

        # Fallback if structure is already separated by newlines
        parts = [p.strip() for p in text.split("\n") if p.strip()]
        if len(parts) >= 2:
            return parts[:4]
        return [clean]

    @staticmethod
    def format_mandiri_inhouse(text: str) -> List[str]:
        """
        Formats In-house Mandiri transfers:
          Line 1: Transfer dari BANK MANDIRI / Transfer ke BANK MANDIRI / Transfer antar Mandiri
          Line 2: [NAME] [ACCOUNT_NUMBER]
        """
        clean = " ".join(text.split())
        m = re.search(r"(Transfer\s+(?:dari\s+BANK\s+MANDIRI|ke\s+BANK\s+MANDIRI|antar\s+Mandiri))\s+(.*)", clean, re.IGNORECASE)
        if m:
            hdr = m.group(1).strip()
            if "antar mandiri" in hdr.lower():
                hdr = "Transfer antar Mandiri"
            elif "dari" in hdr.lower():
                hdr = "Transfer dari BANK MANDIRI"
            elif "ke" in hdr.lower():
                hdr = "Transfer ke BANK MANDIRI"
            return [hdr, m.group(2).strip()]
        parts = [p.strip() for p in text.split("\n") if p.strip()]
        if len(parts) >= 2:
            return parts[:2]
        return [clean]

    @staticmethod
    def format_atm_withdrawal(text: str) -> List[str]:
        """
        Formats ATM cash withdrawals:
          If cardless:
            Line 1: Penarikan tunai tanpa kartu
            Line 2: Di ATM [LOCATION]
            Line 3: [PHONE_NUMBER]
          If debit card:
            Line 1: Penarikan tunai di ATM
            Line 2: BANK MANDIRI [LOCATION_ID]
        """
        clean = " ".join(text.split())

        # Cardless withdrawal
        if "tanpa kartu" in clean.lower():
            m = re.search(r"(Penarikan\s+tunai\s+tanpa\s+kartu)\s+(Di\s+ATM\s+.*?)\s+(\d{10,13})$", clean, re.IGNORECASE)
            if m:
                return [m.group(1).strip(), m.group(2).strip(), m.group(3).strip()]
            parts = [p.strip() for p in text.split("\n") if p.strip()]
            if len(parts) >= 2:
                return parts[:3]

        # Standard ATM withdrawal
        m = re.search(r"(Penarikan\s+tunai\s+di\s+ATM(?: Merah Putih)?)\s+(.*)", clean, re.IGNORECASE)
        if m:
            return [m.group(1).strip(), m.group(2).strip()]

        parts = [p.strip() for p in text.split("\n") if p.strip()]
        if len(parts) >= 2:
            return parts[:2]
        return [clean]

    @staticmethod
    def format_qris_payment(text: str) -> List[str]:
        """
        Formats QRIS transactions:
          Line 1: Pembayaran QR
          Line 2: ke [MERCHANT_NAME]
          Line 3: [REF_ID / CODE]
        """
        clean = " ".join(text.split())
        m = re.search(r"(Pembayaran\s+QR)\s+(ke\s+.*?)\s+(\d{10,16})$", clean, re.IGNORECASE)
        if m:
            return [m.group(1).strip(), m.group(2).strip(), m.group(3).strip()]
        parts = [p.strip() for p in text.split("\n") if p.strip()]
        if len(parts) == 3:
            return parts
        return [clean]

    @staticmethod
    def format_ecommerce(text: str) -> List[str]:
        """
        Formats e-Commerce payments:
          Line 1: Pembayaran [PLATFORM_NAME]
          Line 2: [BILLING/REF_CODE]
        """
        clean = " ".join(text.split())
        m = re.search(r"(Pembayaran\s+(?:Shopee Indonesia|Tokopedia|TikTok|Blibli|Lazada))\s+(.*)", clean, re.IGNORECASE)
        if m:
            return [m.group(1).strip(), m.group(2).strip()]
        parts = [p.strip() for p in text.split("\n") if p.strip()]
        if len(parts) >= 2:
            return parts[:2]
        return [clean]

    @staticmethod
    def format_ewallet_biller(text: str) -> List[str]:
        """
        Formats E-Wallet and Biller transactions:
          Line 1: Pembayaran Danatopup / Pembayaran Instamoney / Top-up e-money
          Line 2: [ACCOUNT_NUMBER / CODE]
        """
        clean = " ".join(text.split())
        m = re.search(r"(Pembayaran\s+[A-Za-z0-9]+|Top-up\s+[A-Za-z0-9\-]+)\s+(\d{10,20})$", clean, re.IGNORECASE)
        if m:
            return [m.group(1).strip(), m.group(2).strip()]
        parts = [p.strip() for p in text.split("\n") if p.strip()]
        if len(parts) >= 2:
            return parts[:2]
        return [clean]

    @staticmethod
    def format_bank_fees(text: str) -> List[str]:
        """Bank fees and administration are strictly 1 line (or 2-3 if biller fee)."""
        clean = " ".join(text.split())
        
        # 3-line Biller Fee e.g. Biaya transaksi bank Pembayaran Danatopup 89508089622130569
        m_biller = re.search(r"(Biaya\s+transaksi\s+bank)\s+(Pembayaran\s+[A-Za-z0-9]+)\s+(\d+)$", clean, re.IGNORECASE)
        if m_biller:
            return [m_biller.group(1).strip(), m_biller.group(2).strip(), m_biller.group(3).strip()]

        # 2-line Payment Fee e.g. Biaya pembayaran ...
        if "Biaya pembayaran" in clean:
            m = re.search(r"(Biaya\s+pembayaran\s+.*?)\s+(\d+)$", clean)
            if m:
                return [m.group(1).strip(), m.group(2).strip()]

        parts = [p.strip() for p in text.split("\n") if p.strip()]
        if len(parts) >= 2:
            return parts[:3]

        return [clean]
