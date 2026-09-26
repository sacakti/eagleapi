"""
Report Widget
-------------
Displays execution summary and assertion results.
"""
from __future__ import annotations
from textual.containers import Vertical
from textual.widgets import DataTable
from textual.widgets import Static

class ReportWidget(Vertical):
    DEFAULT_CSS = """
    ReportWidget {
        height: 1fr;
    }
    #summary {
        height: 4;
        border: round green;
        padding: 0 1;
    }
    #assertions {
        height: 1fr;
        border: round cyan;
    }
    """
    def compose(self):
        yield Static(
            "Execution Report",
            id="summary"
        )
        table = DataTable(
            id="details"
        )
        table.add_columns(
            "Property",
            "Value",
            # "Message"
        )
        yield table
    # --------------------------------------------------
    def clear(self):
        self.query_one(
            "#summary",
            Static
        ).update(
            "Execution Report"
        )
        table = self.query_one(
            "#details",
            DataTable
        )
        table.clear()
    # --------------------------------------------------
    # def show_report(
        # self,
        # result
    # ):
        # passed = sum(
            # 1
            # for assertion in result.assertions
            # if assertion.passed
        # )
        # failed = len(result.assertions) - passed
        # summary = (
            # f"Status : {result.status_code}   "
            # f"Elapsed : {result.elapsed:.2f} ms   "
            # f"Assertions : {passed}/{len(result.assertions)}   "
            # f"Passed : {passed}   "
            # f"Failed : {failed}"
        # )
        # self.query_one(
            # "#summary",
            # Static
        # ).update(summary)
        # table = self.query_one(
            # "#assertions",
            # DataTable
        # )
        # table.clear()
        # for assertion in result.assertions:
            # table.add_row(
                # assertion.name,
                # "✓ PASS" if assertion.passed else "✗ FAIL",
                # assertion.message
            # )
    def show_report(self, result):
       summary = self.query_one(
           "#summary",
           Static
       )
       summary.update(
           f"""
    Status      : {result.status.name}
    HTTP        : {result.http_status}
    Elapsed     : {result.response_time_ms:.2f} ms
    Response    : {result.response_size:,} Bytes
    """
       )
       table = self.query_one(
           "#details",
           DataTable
       )
       table.clear()
       # table.add_columns(
           # "Property",
           # "Value"
       # )
       table.add_row(
           "Endpoint",
           result.endpoint
       )
       table.add_row(
           "Request",
           result.request_name
       )
       table.add_row(
           "Status",
           result.status.name
       )
       table.add_row(
           "HTTP",
           str(result.http_status)
       )
       table.add_row(
           "Response Time",
           f"{result.response_time_ms:.2f} ms"
       )
       table.add_row(
           "Response Size",
           f"{result.response_size:,} Bytes"
       )