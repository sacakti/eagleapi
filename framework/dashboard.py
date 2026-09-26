"""
Enterprise Live Dashboard
Responsibilities
----------------
* Live execution dashboard
* Timeline
* Progress
* Execution statistics
* Current request information
Author : API Tester
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any
from rich.console import Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
   Progress,
   SpinnerColumn,
   BarColumn,
   TextColumn,
   TimeElapsedColumn
)
from rich.table import Table
from rich.text import Text

# =====================================================
# Dashboard State
# =====================================================
@dataclass
class DashboardState:
    execution_id: str = ""
    environment: str = ""
    endpoint: str = ""
    current_request: str = ""
    current_method: str = ""
    current_url: str = ""
    current_phase: str = "Idle"
    current_action: str = ""
    current_status: str = ""
    current_response_time: float = 0.0
    response_size: int = 0
    progress_current: int = 0
    progress_total: int = 0
    passed: int = 0
    failed: int = 0
    average: float = 0.0
    fastest: float = 0.0
    slowest: float = 0.0
    started: datetime = field(default_factory=datetime.now)
    timeline: deque = field(
        default_factory=lambda: deque(maxlen=12)
    )
    def add_event(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.timeline.append(
            (
                timestamp,
                message
            )
        )

# =====================================================
# Dashboard
# =====================================================
class Dashboard:
    REFRESH_PER_SECOND = 5
    def __init__(self):
        self.state = DashboardState()
        self._layout = Layout()
        self._live: Optional[Live] = None
        #
        # Embedded Rich Progress
        #
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[cyan]{task.description}"),
            BarColumn(bar_width=None),
            TextColumn(
                "[bold]{task.completed}/{task.total}"
            ),
            TimeElapsedColumn(),
            expand=True
        )
        self._task_id: Optional[int] = None
    # =================================================
    # Live Lifecycle
    # =================================================
    def start(self):
        if self._live:
            return
        self._live = Live(
            self._render(),
            refresh_per_second=self.REFRESH_PER_SECOND,
            screen=False,
            transient=False
        )
        self._live.start()
    def stop(self):
        if self._live:
            self._live.stop()
            self._live = None
    def refresh(self):
        if self._live:
            self._live.update(
                self._render()
            )
    # =================================================
    # Generic Update
    # =================================================
    def update(
        self,
        **kwargs: Any
    ):
        for key, value in kwargs.items():
            if hasattr(self.state, key):
                setattr(
                    self.state,
                    key,
                    value
                )
        self.refresh()
    # =================================================
    # Timeline
    # =================================================
    def event(
        self,
        message: str
    ):
        self.state.add_event(
            message
        )
        self.refresh()
    # =================================================
    # Progress
    # =================================================
    def progress_start(
        self,
        total: int,
        description: str = "Executing Requests"
    ):
        if self._task_id is not None:
            return
        self._progress.start()
        self._task_id = self._progress.add_task(
            description,
            total=total
        )
        self.update(
            progress_current=0,
            progress_total=total
        )
    def progress_update(
        self,
        description: str = ""
    ):
        if self._task_id is None:
            return
        self._progress.advance(
            self._task_id
        )
        if description:
            self._progress.update(
                self._task_id,
                description=description
            )
        self.state.progress_current += 1
        self.refresh()
    def progress_stop(self):
        if self._task_id is None:
            return
        self._progress.stop()
        self._task_id = None
    # =================================================
    # Convenience Methods
    # =================================================
    def phase(
        self,
        phase: str
    ):
        self.update(
            current_phase=phase
        )
        self.event(
            phase
        )
    def request(
        self,
        request_name: str,
        method: str,
        url: str
    ):
        self.update(
            current_request=request_name,
            current_method=method,
            current_url=url
        )
    def response(
        self,
        status: str,
        response_time: float,
        response_size: int
    ):
        self.update(
            current_status=status,
            current_response_time=response_time,
            response_size=response_size
        )
    def statistics(
        self,
        passed: int,
        failed: int,
        average: float,
        fastest: float,
        slowest: float
    ):
        self.update(
            passed=passed,
            failed=failed,
            average=average,
            fastest=fastest,
            slowest=slowest
        )
        
    # =================================================
    # Render Methods
    # =================================================
    def _header_panel(self):
        table = Table.grid(expand=True)
        table.add_column(style="cyan", width=18)
        table.add_column()
        elapsed = datetime.now() - self.state.started
        table.add_row(
            "Execution",
            self.state.execution_id or "-"
        )
        table.add_row(
            "Environment",
            self.state.environment or "-"
        )
        table.add_row(
            "Endpoint",
            self.state.endpoint or "-"
        )
        table.add_row(
            "Elapsed",
            str(elapsed).split(".")[0]
        )
        return Panel(
            table,
            title="[bold cyan]API TESTER[/bold cyan]",
            border_style="cyan"
        )
    # -------------------------------------------------
    def _request_panel(self):
        table = Table.grid(expand=True)
        table.add_column(style="cyan", width=15)
        table.add_column()
        table.add_row(
            "Request",
            self.state.current_request or "-"
        )
        table.add_row(
            "Method",
            self.state.current_method or "-"
        )
        table.add_row(
            "URL",
            self.state.current_url or "-"
        )
        table.add_row(
            "Phase",
            self.state.current_phase or "-"
        )
        table.add_row(
            "Status",
            self.state.current_status or "-"
        )
        table.add_row(
            "Response",
            f"{self.state.current_response_time:.2f} ms"
            if self.state.current_response_time
            else "-"
        )
        table.add_row(
            "Downloaded",
            f"{self.state.response_size:,} Bytes"
            if self.state.response_size
            else "-"
        )
        return Panel(
            table,
            title="[green]Current Request[/green]",
            border_style="green"
        )
    # -------------------------------------------------
    def _statistics_panel(self):
        table = Table.grid(expand=True)
        table.add_column(style="cyan", width=18)
        table.add_column()
        table.add_row(
            "Progress",
            f"{self.state.progress_current}/{self.state.progress_total}"
        )
        table.add_row(
            "Passed",
            f"[green]{self.state.passed}[/green]"
        )
        table.add_row(
            "Failed",
            f"[red]{self.state.failed}[/red]"
        )
        table.add_row(
            "Average",
            f"{self.state.average:.2f} ms"
        )
        table.add_row(
            "Fastest",
            f"{self.state.fastest:.2f} ms"
        )
        table.add_row(
            "Slowest",
            f"{self.state.slowest:.2f} ms"
        )
        return Panel(
            table,
            title="[yellow]Statistics[/yellow]",
            border_style="yellow"
        )
    # -------------------------------------------------
    def _progress_panel(self):
        if self._task_id is None:
            return Panel(
                Text("Waiting for execution..."),
                title="Progress",
                border_style="blue"
            )
        return Panel(
            self._progress,
            title="Progress",
            border_style="blue"
        )
    # -------------------------------------------------
    def _timeline_panel(self):
        if not self.state.timeline:
            return Panel(
                Text("No events yet."),
                title="Timeline",
                border_style="magenta"
            )
        events = []
        for timestamp, message in self.state.timeline:
            events.append(
                Text(
                    f"{timestamp}  {message}"
                )
            )
        return Panel(
            Group(*events),
            title="[magenta]Timeline[/magenta]",
            border_style="magenta"
        )
    # -------------------------------------------------
    def _render(self):
        self._layout.split_column(
            Layout(
                self._header_panel(),
                size=8
            ),
            Layout(
                name="body",
                size=12
            ),
            Layout(
                self._progress_panel(),
                size=5
            ),
            Layout(
                self._timeline_panel()
            )
        )
        self._layout["body"].split_row(
            Layout(
                self._request_panel()
            ),
            Layout(
                self._statistics_panel()
            )
        )
        return self._layout