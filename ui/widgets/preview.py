"""
Request Preview Widget
"""
from __future__ import annotations
from textual.containers import Vertical
from textual.widgets import Label
from textual.widgets import TextArea
class PreviewPanel(Vertical):
    def __init__(
        self,
        controller,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._controller = controller
        self._title = Label(
            "📝 Request Preview",
            id="preview-title"
        )
        self._editor = TextArea.code_editor(
            text="",
            language="json",
            id="json-preview"
        )
        #
        # Preview only
        #
        self._editor.read_only = True
    # -------------------------------------------------
    def compose(self):
        yield self._title
        yield self._editor
    # -------------------------------------------------
    def clear(self):
        self._editor.text = ""
    # -------------------------------------------------
    def refresh_preview(self):
        text = self._controller.load_request_json()
        if text is None:
            text = ""
        self._editor.text = text
    # -------------------------------------------------
    def set_text(
        self,
        text: str
    ):
        self._editor.text = text
    # -------------------------------------------------
    def get_text(self):
        return self._editor.text
    # -------------------------------------------------
    def set_read_only(
        self,
        value: bool
    ):
        self._editor.read_only = value
    # -------------------------------------------------
    def focus_editor(self):
        self._editor.focus()
 