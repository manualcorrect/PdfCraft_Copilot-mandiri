"""
Corpus Harvester
Extracts authentic transaction descriptions, line breaks, spatial coordinates,
and contextual classifications from official Bank Mandiri e-Statements.
"""

import os
import sys
import json
import re
from typing import Any, Dict, List, Tuple
import pdfplumber

REFERENCE_FILES = [
    r"D:\X_Files\rekening\Reference\Roy\ilovepdf_unlocked\Agu 2026_unlocked.pdf",
    r"D:\X_Files\rekening\Reference\Roy\ilovepdf_unlocked\Mei 2026_unlocked.pdf",
    r"D:\X_Files\rekening\Reference\nasih 2024 new unlocked\ilovepdf_unlocked\e-Statement_XXXXXXXXX9210_01 Des 2024-31 Des 2024_unlocked.pdf",
    r"D:\X_Files\rekening\Reference\suhanda unlocked\e-Statement_XXXXXXXXX9648_01 Apr 2026-30 Apr 2026_unlocked.pdf",
]


def classify_category(full_text: str, lines: List[str]) -> str:
    """Classifies a transaction description into a standard taxonomy."""
    # Check for Corporate Payroll / Salary
    if "PT BENDI NASHA NIAGA INDUSTRI" in full_text or "UPAH" in full_text or "GAJI" in full_text:
        return "PAYROLL_CORPORATE"
    
    if "Transfer BI Fast" in full_text or "Transfer BI FAST" in full_text:
        return "BI_FAST"
    
    if "Transfer" in full_text and "BANK MANDIRI" in full_text:
        return "MANDIRI_INHOUSE"
        
    if "Penarikan tunai" in full_text:
        return "ATM_WITHDRAWAL"
        
    if "Pembayaran QR" in full_text:
        return "QRIS_PAYMENT"
        
    if any(k in full_text for k in ["Shopee Indonesia", "Tokopedia", "TikTok", "Blibli", "Lazada"]):
        return "ECOMMERCE"
        
    if any(k in full_text for k in ["Danatopup", "Instamoney", "Top-up e-money", "Gopay", "OVO", "DANA", "Telkomsel", "PLN"]):
        return "EWALLET_BILLER"
        
    if any(k in full_text for k in ["Biaya", "Bunga", "Pajak"]):
        return "BANK_FEES_ADMIN"
        
    return "GENERAL_TRANSFER"


def harvest_corpus(output_json_path: str) -> List[Dict[str, Any]]:
    """Harvests descriptions across all authentic reference PDFs."""
    corpus: List[Dict[str, Any]] = []

    for f_path in REFERENCE_FILES:
        if not os.path.exists(f_path):
            continue
        
        f_name = os.path.basename(f_path)
        print(f"[Harvester] Scanning {f_name}...")
        
        try:
            with pdfplumber.open(f_path) as pdf:
                for page_idx, page in enumerate(pdf.pages):
                    words = page.extract_words()
                    min_y = 320 if page_idx == 0 else 200
                    max_y = 780
                    table_words = [w for w in words if min_y <= w['top'] <= max_y]

                    base_start = 343.92 if page_idx == 0 else 227.92
                    max_rows = 10 if page_idx == 0 else 12

                    for r_i in range(max_rows):
                        row_y = base_start + r_i * 46.00
                        row_desc_words = [w for w in table_words if 120 <= w['x0'] <= 360 and abs(w['top'] - row_y) < 22.0]
                        if not row_desc_words:
                            continue

                        # Verify row has transaction number or nominal
                        has_row_elem = any(
                            (w['x0'] < 35 and w['text'].isdigit()) or 
                            (w['x0'] >= 350 and (w['text'].startswith('+') or w['text'].startswith('-')))
                            for w in table_words if abs(w['top'] - row_y) < 22.0
                        )
                        if not has_row_elem:
                            continue

                        # Extract Nominal & Tipe
                        nom_words = [w for w in table_words if 350 <= w['x0'] <= 450 and abs(w['top'] - row_y) < 22.0]
                        nom_str = nom_words[0]['text'] if nom_words else ""
                        tipe = "CR" if nom_str.startswith('+') else ("DB" if nom_str.startswith('-') else "UNKNOWN")

                        # Group description words into lines
                        lines_map: Dict[float, List[Dict[str, Any]]] = {}
                        for w in row_desc_words:
                            matched = False
                            for y_k in lines_map:
                                if abs(w['top'] - y_k) < 3.0:
                                    lines_map[y_k].append(w)
                                    matched = True
                                    break
                            if not matched:
                                lines_map[w['top']] = [w]

                        line_strs = []
                        line_bboxes = []
                        for y_k in sorted(lines_map.keys()):
                            sorted_w = sorted(lines_map[y_k], key=lambda x: x['x0'])
                            l_str = " ".join([w['text'] for w in sorted_w])
                            x0 = min(w['x0'] for w in sorted_w)
                            x1 = max(w['x1'] for w in sorted_w)
                            top = min(w['top'] for w in sorted_w)
                            bottom = max(w['bottom'] for w in sorted_w)
                            line_strs.append(l_str)
                            line_bboxes.append({
                                "text": l_str,
                                "x0": round(x0, 2),
                                "x1": round(x1, 2),
                                "width": round(x1 - x0, 2),
                                "top": round(top, 2),
                                "bottom": round(bottom, 2),
                                "rel_y": round(top - row_y, 2)
                            })

                        if not line_strs:
                            continue

                        full_text = "\n".join(line_strs)
                        category = classify_category(full_text, line_strs)

                        corpus.append({
                            "source_file": f_name,
                            "page": page_idx + 1,
                            "row": r_i + 1,
                            "category": category,
                            "line_count": len(line_strs),
                            "full_text": full_text,
                            "lines": line_strs,
                            "line_details": line_bboxes,
                            "tipe": tipe,
                            "nominal": nom_str,
                            "row_base_y": round(row_y, 2)
                        })
        except Exception as e:
            print(f"[Harvester] Error processing {f_name}: {e}")

    # Deduplicate entries by identical (category, full_text)
    unique_corpus = []
    seen = set()
    for item in corpus:
        key = (item["category"], item["full_text"])
        if key not in seen:
            seen.add(key)
            unique_corpus.append(item)

    print(f"[Harvester] Total extracted samples: {len(corpus)}, Unique: {len(unique_corpus)}")
    
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(unique_corpus, f, indent=2, ensure_ascii=False)
        
    print(f"[Harvester] Ground truth corpus saved to: {output_json_path}")
    return unique_corpus


if __name__ == "__main__":
    out_path = os.path.join(os.path.dirname(__file__), "ground_truth_corpus.json")
    harvest_corpus(out_path)
