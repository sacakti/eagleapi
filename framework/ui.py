"""
Console UI utilities.
"""

from __future__ import annotations
from typing import List
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.prompt import Prompt
from rich.table import Table
from rich.align import Align
from rich.panel import Panel
from rich.text import Text

class ApiUI:
    def __init__(self):
        self.console = Console()
    # -------------------------------------------------
    # Banner
    # -------------------------------------------------
    def banner(self):
        
        title = Text(justify="center")
        
        title.append(
            "API TESET v1.0.0\n",
            style="bold cyan"
        )
        
        title.append(
            "Enterprise API Testing Framework",
            style="white"
        )
        
        panel = Panel(
            Align.center(title),
            border_style="cyan",
            padding=(1,6),
            width=70
        )
        
        self.console.print()
        self.console.print(
            Align.center(panel)
        )
        self.console.print()
        
    # -------------------------------------------------
    # Messages
    # -------------------------------------------------
    def success(self, message: str):
        self.console.print(
            f"[green]✓[/green] {message}"
        )
    def warning(self, message: str):
        self.console.print(
            f"[yellow]⚠[/yellow] {message}"
        )
    def error(self, message: str):
        self.console.print(
            f"[red]✗[/red] {message}"
        )
    def info(self, message: str):
        self.console.print(
            f"[cyan]•[/cyan] {message}"
        )
    # -------------------------------------------------
    # Endpoint Table
    # -------------------------------------------------
    def show_endpoints(
        self,
        endpoints
    ):
        table = Table(
            title="Available Endpoints"
        )
        table.add_column(
            "No",
            justify="right",
            width=5
        )
        table.add_column(
            "Endpoint"
        )
        table.add_column(
            "Path"
        )
        table.add_column(
            "Requests",
            justify="right"
        )
        for index, endpoint in enumerate(
            endpoints,
            start=1
        ):
            table.add_row(
                str(index),
                endpoint.name,
                endpoint.path,
                str(endpoint.request_count)
            )
        self.console.print(table)
    # -------------------------------------------------
    # Request Table
    # -------------------------------------------------
    def show_requests(
        self,
        requests
    ):
        table = Table(
            title="Available Requests"
        )
        table.add_column(
            "No",
            justify="right",
            width=5
        )
        table.add_column(
            "Scenario"
        )
        table.add_column(
            "Method"
        )
        table.add_column(
            "Enabled"
        )
        for index, request in enumerate(
            requests,
            start=1
        ):
            table.add_row(
                str(index),
                request.name,
                request.method,
                "✓" if request.enabled else "✗"
            )
        table.add_row(
            "A",
            "Run All",
            "",
            ""
        )
        self.console.print(table)
    # -------------------------------------------------
    # Summary
    # -------------------------------------------------
    def summary(
        self,
        statistics
    ):
        table = Table(
            title="Execution Summary"
        )
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row(
            "Passed",
            str(statistics.passed)
        )
        table.add_row(
            "Failed",
            str(statistics.failed)
        )
        table.add_row(
            "Average",
            f"{statistics.average_response_time:.2f} ms"
        )
        table.add_row(
            "Fastest",
            f"{statistics.fastest_response:.2f} ms"
        )
        table.add_row(
            "Slowest",
            f"{statistics.slowest_response:.2f} ms"
        )
        self.console.print(table)
    # -------------------------------------------------
    # Input
    # -------------------------------------------------
    def ask(
        self,
        message: str
    ) -> str:
        return Prompt.ask(
            message
        )
    def confirm(
        self,
        message: str
    ) -> bool:
        return Confirm.ask(
            message
        )
    # -------------------------------------------------
    # Blank Line
    # -------------------------------------------------
    def newline(self):
        self.console.print()
 