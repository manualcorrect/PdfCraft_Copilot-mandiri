import os
import shutil
import sys
import openpyxl

sys.path.insert(0, 'src')
from pdfcraft_client import PdfCraftClient
from bank_mandiri_spec import (
    COL_NOMINAL_RIGHT_X,
    COL_SALDO_RIGHT_X,
    SUMMARY_RIGHT_X,
    COL_DATE_TIME_X0,
    VALUE_COL1_X0,
    VALUE_COL2_X0,
    VALUE_ACC_X0,
    COLOR_CREDIT_GREEN,
    COLOR_RUNNING_SALDO_BLUE,
    COLOR_DEBIT_BLACK,
    COLOR_SALDO_AWAL_GRAY
)

BASE_DIR = r"D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\keisya\Folder Baru\okt"
PDF_IN = os.path.join(BASE_DIR, "0.pdf")
TEST_OUT = r"c:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\test_step3.pdf"
shutil.copyfile(PDF_IN, TEST_OUT)

with PdfCraftClient() as client:
    doc_id = client.doc_open(TEST_OUT)
    
    # Check headers on pages 1..6
    for p_num in range(1, 7):
        paras = client.get_paragraphs(doc_id, page=p_num)
        
        # Name
        p_name = [p for p in paras if "ROY DARWIN REZERIUS" in p["text"] and p["rect"][1] < 115]
        if p_name:
            client.edit_text(doc_id, page=p_num, paragraph=p_name[0]["paragraph"], text="KEISYA AULIA")
            up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_name[0]["paragraph"]][0]
            dx = VALUE_COL1_X0 - up["rect"][0]
            if abs(dx) > 0.02: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)
            
        # Branch
        paras = client.get_paragraphs(doc_id, page=p_num)
        p_branch = [p for p in paras if "KCP Jakarta Taman Aries" in p["text"] and p["rect"][1] < 135]
        if p_branch:
            client.edit_text(doc_id, page=p_num, paragraph=p_branch[0]["paragraph"], text="KCP Serang Ciceri")
            up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_branch[0]["paragraph"]][0]
            dx = VALUE_COL1_X0 - up["rect"][0]
            if abs(dx) > 0.02: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)
            
        # Period
        paras = client.get_paragraphs(doc_id, page=p_num)
        p_per = [p for p in paras if "01 Apr 2026 - 30 Apr 2026" in p["text"] and p["rect"][1] < 115]
        if p_per:
            client.edit_text(doc_id, page=p_num, paragraph=p_per[0]["paragraph"], text="01 Oct 2026 - 31 Oct 2026")
            up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_per[0]["paragraph"]][0]
            dx = VALUE_COL2_X0 - up["rect"][0]
            if abs(dx) > 0.02: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)
            
        # Issued on
        paras = client.get_paragraphs(doc_id, page=p_num)
        p_iss = [p for p in paras if "09 Sep 2026" in p["text"] and p["rect"][1] < 135]
        if p_iss:
            client.edit_text(doc_id, page=p_num, paragraph=p_iss[0]["paragraph"], text="12 Nov 2026")
            up = [p for p in client.get_paragraphs(doc_id, page=p_num) if p["paragraph"] == p_iss[0]["paragraph"]][0]
            dx = VALUE_COL2_X0 - up["rect"][0]
            if abs(dx) > 0.02: client.edit_text(doc_id, page=p_num, paragraph=up["paragraph"], dx=dx)

    # Page 1 Summary Box & Account Number
    paras = client.get_paragraphs(doc_id, page=1)
    
    # Account Number
    p_acc = [p for p in paras if "1650003584860" in p["text"]]
    if p_acc:
        client.edit_text(doc_id, page=1, paragraph=p_acc[0]["paragraph"], text="1630016478664")
        up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_acc[0]["paragraph"]][0]
        dx = VALUE_ACC_X0 - up["rect"][0]
        if abs(dx) > 0.02: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

    # Saldo Awal (6.850.820,81)
    paras = client.get_paragraphs(doc_id, page=1)
    p_sawal = [p for p in paras if 160 <= p["rect"][1] <= 180 and p["rect"][0] > 480][0]
    client.edit_text(doc_id, page=1, paragraph=p_sawal["paragraph"], text="6.850.820,81", color=COLOR_SALDO_AWAL_GRAY)
    up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_sawal["paragraph"]][0]
    dx = SUMMARY_RIGHT_X - up["rect"][2]
    if abs(dx) > 0.01: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

    # Dana Masuk (+ 14.306.611,00)
    paras = client.get_paragraphs(doc_id, page=1)
    p_dmasuk = [p for p in paras if 185 <= p["rect"][1] <= 205 and p["rect"][0] > 480][0]
    client.edit_text(doc_id, page=1, paragraph=p_dmasuk["paragraph"], text="+ 14.306.611,00", color=COLOR_CREDIT_GREEN)
    up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_dmasuk["paragraph"]][0]
    dx = SUMMARY_RIGHT_X - up["rect"][2]
    if abs(dx) > 0.01: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

    # Dana Keluar (- 8.446.550,00)
    paras = client.get_paragraphs(doc_id, page=1)
    p_dkeluar = [p for p in paras if 208 <= p["rect"][1] <= 228 and p["rect"][0] > 480][0]
    client.edit_text(doc_id, page=1, paragraph=p_dkeluar["paragraph"], text="- 8.446.550,00", color=COLOR_DEBIT_BLACK)
    up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_dkeluar["paragraph"]][0]
    dx = SUMMARY_RIGHT_X - up["rect"][2]
    if abs(dx) > 0.01: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

    # Saldo Akhir (12.710.881,81)
    paras = client.get_paragraphs(doc_id, page=1)
    p_sakhir = [p for p in paras if 230 <= p["rect"][1] <= 255 and p["rect"][0] > 480][0]
    client.edit_text(doc_id, page=1, paragraph=p_sakhir["paragraph"], text="12.710.881,81", color=COLOR_RUNNING_SALDO_BLUE)
    up = [p for p in client.get_paragraphs(doc_id, page=1) if p["paragraph"] == p_sakhir["paragraph"]][0]
    dx = SUMMARY_RIGHT_X - up["rect"][2]
    if abs(dx) > 0.01: client.edit_text(doc_id, page=1, paragraph=up["paragraph"], dx=dx)

    # Tx 30 (Page 3, Row 35) -> +100.000,00
    paras = client.get_paragraphs(doc_id, page=3)
    p_nom30 = [p for p in paras if abs(p["rect"][1] - 550.0) < 15 and 370 <= p["rect"][0] <= 450]
    if p_nom30:
        client.edit_text(doc_id, page=3, paragraph=p_nom30[0]["paragraph"], text="+100.000,00", color=COLOR_CREDIT_GREEN)
        up_n = [p for p in client.get_paragraphs(doc_id, page=3) if p["paragraph"] == p_nom30[0]["paragraph"]][0]
        dx_n = COL_NOMINAL_RIGHT_X - up_n["rect"][2]
        if abs(dx_n) > 0.01: client.edit_text(doc_id, page=3, paragraph=up_n["paragraph"], dx=dx_n)
        print("Tx 30 updated to +100.000,00")

    # Tx 53 (Page 5, Row 58) -> +6.903.611,00
    paras = client.get_paragraphs(doc_id, page=5)
    p_nom53 = [p for p in paras if abs(p["rect"][1] - 504.0) < 15 and 370 <= p["rect"][0] <= 450]
    if p_nom53:
        client.edit_text(doc_id, page=5, paragraph=p_nom53[0]["paragraph"], text="+6.903.611,00", color=COLOR_CREDIT_GREEN)
        up_n = [p for p in client.get_paragraphs(doc_id, page=5) if p["paragraph"] == p_nom53[0]["paragraph"]][0]
        dx_n = COL_NOMINAL_RIGHT_X - up_n["rect"][2]
        if abs(dx_n) > 0.01: client.edit_text(doc_id, page=5, paragraph=up_n["paragraph"], dx=dx_n)
        print("Tx 53 updated to +6.903.611,00")

    client.doc_save(doc_id)
    print("Test Step 3 completed successfully!")
