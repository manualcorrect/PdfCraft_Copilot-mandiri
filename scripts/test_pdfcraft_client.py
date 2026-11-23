import os
import sys

# Add src to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from pdfcraft_client import PdfCraftClient

def main():
    print("Testing PdfCraftClient initialization...")
    with PdfCraftClient() as client:
        print("PdfCraftClient connected successfully.")
        
        # Test doc_open
        target_pdf = r"C:\Users\Wisnu\.gemini\antigravity\scratch\PdfCraft_Copilot\output\test_save.pdf"
        doc_id = client.doc_open(target_pdf)
        print(f"Opened doc_id: {doc_id}")
        
        # Test doc_info
        info = client.doc_info(doc_id)
        print(f"Doc pages: {info.get('pages')}, encrypted: {info.get('encrypted')}")
        
        # Test get_paragraphs
        paras = client.get_paragraphs(doc_id, page=1)
        print(f"Page 1 has {len(paras)} paragraphs.")
        
        # Test edit_text on first paragraph (dx=0, color unchanged)
        res = client.edit_text(doc_id, page=1, paragraph=1, dx=0.0)
        print(f"Edit paragraph 1 result undo: {res.get('undo')}")
        
        # Close doc
        client.doc_close(doc_id, discard_changes=True)
        print("Doc closed successfully.")

    print("All PdfCraftClient tests passed!")

if __name__ == "__main__":
    main()
