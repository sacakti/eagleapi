"""
Execution Widget
----------------
Displays live execution progress and logs.
"""
from textual.containers import Vertical
from textual.widgets import ProgressBar
from textual.widgets import RichLog

class ExecutionWidget(Vertical):
    DEFAULT_CSS = """
    ExecutionWidget {
        height: 1fr;
    }
    #progress {
        height: 3;
        margin-bottom: 1;
    }
    #log {
        height: 1fr;
        border: round cyan;
    }
    """
    def compose(self):
        yield ProgressBar(
            total=1,
            show_percentage=False,
            show_eta=False,
            id="progress"
        )
        yield RichLog(
            id="log",
            wrap=True,
            highlight=True,
            markup=True,
            auto_scroll=True
        )
    # --------------------------------------------------
    # Reset
    # --------------------------------------------------
    def reset(self):
        progress = self.query_one(
            "#progress",
            ProgressBar
        )
        progress.update(
            progress=0,
            total=1
        )
        log = self.query_one(
            "#log",
            RichLog
        )
        log.clear()
    # --------------------------------------------------
    # Progress
    # --------------------------------------------------
    def set_total(
        self,
        total: int
    ):
        self.query_one(
            "#progress",
            ProgressBar
        ).update(
            total=total,
            progress=0
        )
    def advance(self):
        progress = self.query_one(
            "#progress",
            ProgressBar
        )
        progress.advance(1)
    def update_progress(
        self,
        current: int,
        total: int
    ):
        self.query_one(
            "#progress",
            ProgressBar
        ).update(
            progress=current,
            total=total
        )
    # --------------------------------------------------
    # Logs
    # --------------------------------------------------
    def write(
        self,
        message: str
    ):
        self.query_one(
            "#log",
            RichLog
        ).write(message)
    def info(
        self,
        message: str
    ):
        self.write(
            f"[cyan]{message}[/]"
        )
    def success(
        self,
        message: str
    ):
        self.write(
            f"[green]✓ {message}[/]"
        )
    def warning(
        self,
        message: str
    ):
        self.write(
            f"[yellow]⚠ {message}[/]"
        )
    def error(
        self,
        message: str
    ):
        self.write(
            f"[red]✗ {message}[/]"
        )