"""
PdfCraft Client Bridge
Provides a robust, pythonic JSON-RPC interface to pdfcraft-cli MCP server.
"""

import os
import sys
import json
import subprocess
from typing import Any, Dict, List, Optional, Tuple

PDFCRAFT_CLI_DEFAULT_PATH = os.path.expandvars(
    r"%LOCALAPPDATA%\Programs\PdfCraft\pdfcraft-cli.exe"
)
if not os.path.exists(PDFCRAFT_CLI_DEFAULT_PATH):
    PDFCRAFT_CLI_DEFAULT_PATH = r"C:\Program Files\PdfCraft\pdfcraft-cli.exe"


class PdfCraftClient:
    """Manages a headless connection to the PdfCraft MCP server."""

    def __init__(self, cli_path: str = PDFCRAFT_CLI_DEFAULT_PATH):
        if not os.path.exists(cli_path):
            raise FileNotFoundError(f"PdfCraft CLI not found at: {cli_path}")
        
        self.cli_path = cli_path
        self._process: Optional[subprocess.Popen] = None
        self._msg_id = 0
        self._start_server()

    def _start_server(self):
        """Starts the pdfcraft-cli MCP server process and runs handshake."""
        self._process = subprocess.Popen(
            [self.cli_path, "mcp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        # 1. initialize
        init_res = self._send_request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "PdfCraftCopilot", "version": "1.0.0"}
            }
        )
        if "error" in init_res:
            raise RuntimeError(f"PdfCraft MCP initialization failed: {init_res['error']}")
        
        # 2. notifications/initialized
        self._send_notification("notifications/initialized", {})

    def _send_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Sends a JSON-RPC request and returns the parsed response."""
        self._msg_id += 1
        req = {
            "jsonrpc": "2.0",
            "id": self._msg_id,
            "method": method,
            "params": params or {}
        }
        req_line = json.dumps(req) + "\n"
        self._process.stdin.write(req_line)
        self._process.stdin.flush()

        res_line = self._process.stdout.readline()
        if not res_line:
            stderr_out = self._process.stderr.read()
            raise RuntimeError(f"PdfCraft process closed unexpectedly. Stderr: {stderr_out}")
        return json.loads(res_line)

    def _send_notification(self, method: str, params: Optional[Dict[str, Any]] = None):
        """Sends a JSON-RPC notification (no response expected)."""
        notif = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {}
        }
        notif_line = json.dumps(notif) + "\n"
        self._process.stdin.write(notif_line)
        self._process.stdin.flush()

    def call_tool(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calls a tool via tools/call and returns the tool's result data."""
        res = self._send_request(
            "tools/call",
            {
                "name": name,
                "arguments": arguments or {}
            }
        )
        if "error" in res:
            raise RuntimeError(f"Error calling {name}: {res['error']}")
        
        result_payload = res.get("result", {})
        if result_payload.get("isError"):
            err_msg = ""
            for item in result_payload.get("content", []):
                if item.get("type") == "text":
                    err_msg += item.get("text", "")
            raise RuntimeError(f"Tool {name} returned error: {err_msg}")
        
        # Prefer structuredContent if provided, otherwise parse JSON from text content
        if "structuredContent" in result_payload:
            return result_payload["structuredContent"]
        
        content_items = result_payload.get("content", [])
        if content_items and content_items[0].get("type") == "text":
            try:
                return json.loads(content_items[0]["text"])
            except json.JSONDecodeError:
                return {"text": content_items[0]["text"]}
        return result_payload

    # High-level convenience methods

    def doc_open(self, path: str, password: Optional[str] = None) -> int:
        """Opens a PDF and returns the assigned integer doc id."""
        args = {"path": path}
        if password:
            args["password"] = password
        res = self.call_tool("doc_open", args)
        return res["doc"]

    def doc_list(self) -> List[Dict[str, Any]]:
        """Lists all open documents."""
        res = self.call_tool("doc_list")
        return res.get("documents", [])

    def doc_info(self, doc_id: int) -> Dict[str, Any]:
        """Gets metadata, page dimensions, fonts, etc."""
        return self.call_tool("doc_info", {"doc": doc_id})

    def doc_save(self, doc_id: int, path: Optional[str] = None, full: bool = True) -> Dict[str, Any]:
        """Saves document to current or new path."""
        args = {"doc": doc_id, "full": full}
        if path:
            args["path"] = path
        return self.call_tool("doc_save", args)

    def doc_close(self, doc_id: int, discard_changes: bool = False) -> Dict[str, Any]:
        """Closes the open document."""
        return self.call_tool("doc_close", {"doc": doc_id, "discard_changes": discard_changes})

    def get_paragraphs(self, doc_id: int, page: int) -> List[Dict[str, Any]]:
        """Retrieves all paragraphs with coordinates, fonts, and text for a page."""
        res = self.call_tool("text_paragraphs", {"doc": doc_id, "page": page})
        return res.get("paragraphs", [])

    def edit_text(
        self,
        doc_id: int,
        page: int,
        paragraph: Optional[int] = None,
        line: Optional[int] = None,
        text: Optional[str] = None,
        dx: Optional[float] = None,
        dy: Optional[float] = None,
        color: Optional[str] = None,
        font: Optional[str] = None,
        font_resource: Optional[str] = None,
        bold: Optional[bool] = None,
        italic: Optional[bool] = None,
        size: Optional[float] = None,
        align: Optional[str] = None,
        width: Optional[float] = None,
        char_spacing: Optional[float] = None,
        scale: Optional[float] = None,
        line_spacing: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Edits or shifts a paragraph/line in place."""
        args: Dict[str, Any] = {"doc": doc_id, "page": page}
        if paragraph is not None:
            args["paragraph"] = paragraph
        if line is not None:
            args["line"] = line
        if text is not None:
            args["text"] = text
        if dx is not None:
            args["dx"] = round(dx, 3)
        if dy is not None:
            args["dy"] = round(dy, 3)
        if color is not None:
            args["color"] = color
        if font is not None:
            args["font"] = font
        if font_resource is not None:
            args["font_resource"] = font_resource
        if bold is not None:
            args["bold"] = bold
        if italic is not None:
            args["italic"] = italic
        if size is not None:
            args["size"] = size
        if align is not None:
            args["align"] = align
        if width is not None:
            args["width"] = width
        if char_spacing is not None:
            args["char_spacing"] = char_spacing
        if scale is not None:
            args["scale"] = scale
        if line_spacing is not None:
            args["line_spacing"] = line_spacing

        return self.call_tool("text_edit", args)

    def page_duplicate(self, doc_id: int, page: int) -> Dict[str, Any]:
        """Duplicates a page within the document."""
        return self.call_tool("page_duplicate", {"doc": doc_id, "page": page})

    def page_delete(self, doc_id: int, pages: List[int]) -> Dict[str, Any]:
        """Deletes specified pages (1-based)."""
        return self.call_tool("page_delete", {"doc": doc_id, "pages": pages})

    def page_insert_file(
        self,
        doc_id: int,
        after_page: int,
        path: str,
        pages: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """Inserts pages from an external PDF file after after_page."""
        args: Dict[str, Any] = {
            "doc": doc_id,
            "after_page": after_page,
            "path": path
        }
        if pages:
            args["pages"] = pages
        return self.call_tool("page_insert_file", args)

    def close(self):
        """Terminates the client process."""
        if self._process and self._process.poll() is None:
            try:
                self._process.terminate()
                self._process.wait(timeout=2)
            except Exception:
                self._process.kill()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
