"""
Response Widget
---------------
Displays HTTP response with syntax highlighting.
"""
from __future__ import annotations
import json
from textual.containers import Vertical
from textual.widgets import Static
from textual.widgets import TextArea

class ResponseWidget(Vertical):
    DEFAULT_CSS = """
    ResponseWidget {
        height: 1fr;
    }
    #summary {
        height: 3;
        border: round green;
        padding: 0 1;
    }
    #response {
        height: 1fr;
        border: round cyan;
    }
    """
    def compose(self):
        yield Static(
            "No response received.",
            id="summary"
        )
        editor = TextArea.code_editor(
            "",
            language="json",
            id="response"
        )
        editor.read_only = True
        yield editor
    # --------------------------------------------------
    # Clear
    # --------------------------------------------------
    def clear(self):
        self.query_one(
            "#summary",
            Static
        ).update(
            "No response received."
        )
        self.query_one(
            "#response",
            TextArea
        ).text = ""
    # --------------------------------------------------
    # Display
    # --------------------------------------------------
    def show_response(
        self,
        status_code: int,
        elapsed_ms: float,
        headers: dict,
        body
    ):  
        #print(f"Response tab called")
        summary = (
            f"Status : {status_code}    "
            f"Elapsed : {elapsed_ms:.2f} ms    "
            f"Headers : {len(headers)}"
        )
        self.query_one(
            "#summary",
            Static
        ).update(summary)
        
        #print("checking response type | json or text")
        if isinstance(body, (dict, list)):
            text = json.dumps(
                body,
                indent=4,
                ensure_ascii=False
            )
        else:
            text = str(body)
        
        #print(f"Printing response data : {text}")
        
        self.query_one(
            "#response",
            TextArea
        ).text = text
    # --------------------------------------------------
    # Error
    # --------------------------------------------------
    def show_error(
        self,
        message: str
    ):
        self.query_one(
            "#summary",
            Static
        ).update(
            "[ERROR]"
        )
        self.query_one(
            "#response",
            TextArea
        ).text = message