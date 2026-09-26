"""
Workspace Widget
ui/widgets/workspace.py
Right side of the application.
Contains
   Preview
   Execution
   Response
   Report
"""
from __future__ import annotations
import json
from textual.containers import Vertical
from textual.widgets import RichLog
from textual.widgets import TabbedContent
from textual.widgets import TabPane
from textual.widgets import TextArea

from ui.widgets.execution import ExecutionWidget
from ui.widgets.response import ResponseWidget
from ui.widgets.report import ReportWidget


class Workspace(Vertical):
    def __init__(self, controller):
        super().__init__()
        self._controller = controller
        #
        # Preview
        #
        self._preview = TextArea.code_editor(
            text="",
            language="json",
            read_only=True,
            id="preview-editor"
        )
        #
        # Execution
        #
        # self._execution = RichLog(
            # id="execution-log",
            # wrap=True,
            # highlight=True,
            # markup=True
        # )
        self._execution = ExecutionWidget()
        #
        # Response
        #
        # self._response = TextArea.code_editor(
            # text="",
            # language="json",
            # read_only=True,
            # id="response-editor"
        # )
        self._response = ResponseWidget()
        #
        # Report
        #
        # self._report = RichLog(
            # id="report-log",
            # wrap=True,
            # markup=True
        # )
        self._report = ReportWidget()
        self._tabs = None
    # --------------------------------------------------
    def compose(self):
        with TabbedContent(id="workspace-tabs") as tabs:
            self._tabs = tabs
            with TabPane("Preview", id="preview-tab"):
                yield self._preview
            with TabPane("Execution", id="execution-tab"):
                yield self._execution
            with TabPane("Response", id="response-tab"):
                yield self._response
            with TabPane("Report", id="report-tab"):
                yield self._report
    # ==================================================
    # Preview
    # ==================================================
    def show_preview(self):
        self._tabs.active = "preview-tab"
    def refresh_preview(self):
        request = self._controller.current_request()
        if request is None:
            self._preview.text = ""
            return
        text = json.dumps(
            request.model_dump(
                by_alias=True
            ),
            indent=4,
            ensure_ascii=False
        )
        self._preview.text = text
        # self.show_preview()
    # ==================================================
    # Execution
    # ==================================================
    def show_execution(self):
        self._tabs.active = "execution-tab"
    def clear_execution(self):
        self._execution.reset()
    def execution(self, text: str):
        self._execution.write(text)
    # ==================================================
    # Response
    # ==================================================
    def show_response(self):
        self._tabs.active = "response-tab"
    def clear_response(self):
        self._response.text = ""
    def response(self, body):
        if body is None:
            self._response.text = ""
            return
        if isinstance(body, str):
            self._response.text = body
            return
        self._response.text = json.dumps(
            body,
            indent=4,
            ensure_ascii=False
        )
        self.show_response()
    # ==================================================
    # Report
    # ==================================================
    def show_report(self):
        self._tabs.active = "report-tab"
    def clear_report(self):
        self._report.clear()
    def report(self, text):
        self._report.write(text)
    # ==================================================
    # Edit
    # ==================================================
    def enable_edit(self):
        self._preview.read_only = False
        self._preview.focus()
    def disable_edit(self):
        self._preview.read_only = True
    def preview_text(self):
        return self._preview.text
        
    
    #
    # Show Result
    #
    
    def show_execution_result(
       self,
       result
    ):
        #
        # Execution
        #
        self.show_execution()
        self.clear_execution()
        self._execution.success("Request Completed")
        self._execution.info(
            f"HTTP Status : {result.http_status}"
        )
        self._execution.info(
            f"Response Time : {result.response_time_ms:.2f} ms"
        )
        self._execution.info(
            f"Response Size : {result.response_size:,} Bytes"
        )
        #
        # Response
        #
        self._response.show_response(
            status_code=result.http_status,
            elapsed_ms=result.response_time_ms,
            headers=result.response_headers,
            body=result.response_body
        )
        #
        # Report
        #
        
        self._report.clear()
        
        self._report.show_report(result)