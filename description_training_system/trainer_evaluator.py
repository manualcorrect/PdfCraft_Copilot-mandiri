"""
Trainer & Evaluator
Benchmarks DescriptionModelEngine against the ground truth corpus,
measures pattern accuracy, tests edge cases, and logs structured results.
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# Ensure parent path is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from description_training_system.description_model import DescriptionModelEngine
from description_training_system.syntax_rules import TransactionCategory


class DescriptionTrainerEvaluator:
    """Evaluates and logs description engine performance across reference datasets."""

    def __init__(self, corpus_path: Optional[str] = None, logs_dir: Optional[str] = None):
        module_dir = os.path.dirname(os.path.abspath(__file__))
        if corpus_path is None:
            corpus_path = os.path.join(module_dir, "ground_truth_corpus.json")
        if logs_dir is None:
            logs_dir = os.path.join(module_dir, "training_logs")
            
        self.corpus_path = corpus_path
        self.logs_dir = logs_dir
        self.history_file = os.path.join(logs_dir, "training_history.jsonl")
        self.latest_report_file = os.path.join(logs_dir, "LATEST_TRAINING_REPORT.md")

    def run_training_evaluation(self) -> Dict[str, Any]:
        """Runs evaluation over the ground truth corpus and evaluates edge cases."""
        if not os.path.exists(self.corpus_path):
            raise FileNotFoundError(f"Corpus file not found: {self.corpus_path}")

        with open(self.corpus_path, "r", encoding="utf-8") as f:
            corpus: List[Dict[str, Any]] = json.load(f)

        total_samples = len(corpus)
        category_matches = 0
        line_count_matches = 0
        safety_passes = 0

        breakdown_by_cat: Dict[str, Dict[str, int]] = {}

        for item in corpus:
            raw_text = item["full_text"]
            gt_cat = item["category"]
            gt_line_count = item["line_count"]

            pred = DescriptionModelEngine.format(raw_text)

            cat_match = (pred["category"] == gt_cat)
            line_match = (pred["line_count"] == gt_line_count)
            is_safe = pred["is_safe"]

            if cat_match:
                category_matches += 1
            if line_match:
                line_count_matches += 1
            if is_safe:
                safety_passes += 1

            if gt_cat not in breakdown_by_cat:
                breakdown_by_cat[gt_cat] = {"total": 0, "cat_matched": 0, "line_matched": 0}
            breakdown_by_cat[gt_cat]["total"] += 1
            if cat_match:
                breakdown_by_cat[gt_cat]["cat_matched"] += 1
            if line_match:
                breakdown_by_cat[gt_cat]["line_matched"] += 1

        # Specific Target Benchmarks (Must-Pass Edge Cases)
        edge_cases = self._evaluate_edge_cases()

        cat_acc = (category_matches / total_samples) * 100 if total_samples > 0 else 0
        line_acc = (line_count_matches / total_samples) * 100 if total_samples > 0 else 0
        safety_acc = (safety_passes / total_samples) * 100 if total_samples > 0 else 0

        result_summary = {
            "timestamp": datetime.now().isoformat(),
            "total_samples": total_samples,
            "category_accuracy_pct": round(cat_acc, 2),
            "line_count_accuracy_pct": round(line_acc, 2),
            "layout_safety_pct": round(safety_acc, 2),
            "category_matches": category_matches,
            "line_count_matches": line_count_matches,
            "category_breakdown": breakdown_by_cat,
            "edge_case_results": edge_cases
        }

        # Save to training history and latest report
        self._save_training_log(result_summary)
        self._generate_markdown_report(result_summary)

        return result_summary

    def _evaluate_edge_cases(self) -> List[Dict[str, Any]]:
        """Tests mandatory regression cases specified by user and authentic references."""
        test_cases = [
            {
                "case_id": "TC-01-TX18-PAYROLL",
                "name": "Galang Jul Tx 18 / Salman Apr Row 14 Corporate Payroll",
                "input": "Transfer BI Fast Dari BCA\nPT BENDI NASHA NIAGA INDUSTRI 5411078192\n(CENAIDJA)",
                "expected_lines": [
                    "Transfer BI Fast",
                    "Dari BCA",
                    "PT BENDI NASHA NIAGA INDUSTRI 5411078192",
                    "(CENAIDJA)"
                ],
                "expected_cat": "PAYROLL_CORPORATE"
            },
            {
                "case_id": "TC-02-BIFAST-FLAT",
                "name": "Single-line BI Fast with Bank and Remark",
                "input": "Transfer BI Fast Dari BCA KARINA AMALIA DARMAW 2452998221 CICIL UPAH MEI 2026",
                "expected_lines": [
                    "Transfer BI Fast",
                    "Dari BCA",
                    "KARINA AMALIA DARMAW 2452998221",
                    "CICIL UPAH MEI 2026"
                ],
                "expected_cat": "PAYROLL_CORPORATE" # Contains UPAH
            },
            {
                "case_id": "TC-03-MANDIRI-INHOUSE",
                "name": "In-house Mandiri Transfer with Account Number",
                "input": "Transfer dari BANK MANDIRI SIGIT BUDHI ARYONO 1550009926679",
                "expected_lines": [
                    "Transfer dari BANK MANDIRI",
                    "SIGIT BUDHI ARYONO 1550009926679"
                ],
                "expected_cat": "MANDIRI_INHOUSE"
            },
            {
                "case_id": "TC-04-ATM-CARDLESS",
                "name": "Cardless ATM Cash Withdrawal (3 lines)",
                "input": "Penarikan tunai tanpa kartu Di ATM SRG AM PURI ANGREK 0 089622130569",
                "expected_lines": [
                    "Penarikan tunai tanpa kartu",
                    "Di ATM SRG AM PURI ANGREK 0",
                    "089622130569"
                ],
                "expected_cat": "ATM_WITHDRAWAL"
            },
            {
                "case_id": "TC-05-QR-PAYMENT",
                "name": "QRIS Merchant Payment (3 lines)",
                "input": "Pembayaran QR ke Kantin Ka Rin 507016923183",
                "expected_lines": [
                    "Pembayaran QR",
                    "ke Kantin Ka Rin",
                    "507016923183"
                ],
                "expected_cat": "QRIS_PAYMENT"
            },
            {
                "case_id": "TC-06-BANK-FEE",
                "name": "Single-line Bank Fee",
                "input": "Biaya administrasi rekening",
                "expected_lines": [
                    "Biaya administrasi rekening"
                ],
                "expected_cat": "BANK_FEES_ADMIN"
            }
        ]

        results = []
        for tc in test_cases:
            pred = DescriptionModelEngine.format(tc["input"])
            lines_match = (pred["lines"] == tc["expected_lines"])
            cat_match = (pred["category"] == tc["expected_cat"])
            passed = lines_match and cat_match and pred["is_safe"]

            results.append({
                "case_id": tc["case_id"],
                "name": tc["name"],
                "passed": passed,
                "lines_match": lines_match,
                "cat_match": cat_match,
                "pred_lines": pred["lines"],
                "expected_lines": tc["expected_lines"],
                "pred_cat": pred["category"],
                "expected_cat": tc["expected_cat"],
                "target_top_offset": pred["target_top_offset"]
            })

        return results

    def _save_training_log(self, summary: Dict[str, Any]):
        """Appends result to training_history.jsonl."""
        os.makedirs(self.logs_dir, exist_ok=True)
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(summary, ensure_ascii=False) + "\n")

    def _generate_markdown_report(self, summary: Dict[str, Any]):
        """Generates comprehensive human-readable report."""
        edge_pass_count = sum(1 for e in summary["edge_case_results"] if e["passed"])
        total_edges = len(summary["edge_case_results"])

        md = f"""# Laporan Monitoring Sistem Logika Training Keterangan
**Waktu Eksekusi:** `{summary['timestamp']}`  
**Dataset Ground Truth:** `{summary['total_samples']} Sampel Transaksi Resmi Bank Mandiri`

---

## 1. Ringkasan Metrik Akurasi & Keamanan Spasial

| Metrik Evaluasi | Hasil Model | Target Baku | Status |
| :--- | :---: | :---: | :---: |
| **Akurasi Klasifikasi Kategori** | **{summary['category_accuracy_pct']}%** | $\\ge 95.0\\%$ | {'✅ PASS' if summary['category_accuracy_pct'] >= 95 else '⚠️ REVIEW'} |
| **Akurasi Pemisahan Baris (Line Count)** | **{summary['line_count_accuracy_pct']}%** | $\\ge 95.0\\%$ | {'✅ PASS' if summary['line_count_accuracy_pct'] >= 95 else '⚠️ REVIEW'} |
| **Kepatuhan Keamanan Spasial (Zero-Collision)** | **{summary['layout_safety_pct']}%** | $100.0\\%$ | {'✅ PASS' if summary['layout_safety_pct'] == 100 else '⚠️ WARN'} |
| **Hasil Uji Kasus Khusus (Edge Cases)** | **{edge_pass_count} / {total_edges}** | $100\\%$ | {'✅ SEMUA LULUS' if edge_pass_count == total_edges else '❌ GAGAL'} |

---

## 2. Performa Berdasarkan Kategori Transaksi

| Kategori Transaksi | Total Sampel | Akurasi Kategori | Akurasi Format Baris |
| :--- | :---: | :---: | :---: |
"""
        for cat, data in sorted(summary["category_breakdown"].items()):
            tot = data["total"]
            c_acc = (data["cat_matched"] / tot) * 100 if tot > 0 else 0
            l_acc = (data["line_matched"] / tot) * 100 if tot > 0 else 0
            md += f"| `{cat}` | {tot} | {c_acc:.1f}% | {l_acc:.1f}% |\n"

        md += """
---

## 3. Hasil Pengujian Kasus Khusus (Mandatory Regression Tests)

"""
        for tc in summary["edge_case_results"]:
            status_emoji = "✅ PASS" if tc["passed"] else "❌ FAIL"
            md += f"### {tc['case_id']}: {tc['name']} [{status_emoji}]\n"
            md += f"- **Kategori Prediksi:** `{tc['pred_cat']}` (Target: `{tc['expected_cat']}`)\n"
            md += f"- **Offset Vertikal ($dY$):** `{tc['target_top_offset']} pt` dari garis dasar baris\n"
            md += "- **Penyusunan Baris Prediksi:**\n"
            for i, l in enumerate(tc["pred_lines"]):
                md += f"  {i+1}. `{l}`\n"
            if not tc["lines_match"]:
                md += "- **Target Baris Diharapkan:**\n"
                for i, l in enumerate(tc["expected_lines"]):
                    md += f"  {i+1}. `{l}`\n"
            md += "\n"

        md += """---
*Laporan ini dihasilkan secara otomatis oleh `DescriptionTrainerEvaluator` dan tersimpan secara permanen pada log monitoring.*
"""

        with open(self.latest_report_file, "w", encoding="utf-8") as f:
            f.write(md)


if __name__ == "__main__":
    evaluator = DescriptionTrainerEvaluator()
    res = evaluator.run_training_evaluation()
    print("=" * 60)
    print("   TRAINING EVALUATION COMPLETED")
    print("=" * 60)
    print(f"Total Samples    : {res['total_samples']}")
    print(f"Category Accuracy: {res['category_accuracy_pct']}%")
    print(f"Line Accuracy    : {res['line_count_accuracy_pct']}%")
    print(f"Layout Safety    : {res['layout_safety_pct']}%")
    print("\nEdge Case Results:")
    for ec in res["edge_case_results"]:
        status = "PASS" if ec["passed"] else "FAIL"
        print(f"  [{status}] {ec['case_id']}: {ec['name']}")
