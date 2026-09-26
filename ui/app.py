"""
API Tester
Textual Application
"""
from __future__ import annotations
import platform
import uuid
from pathlib import Path
from textual.app import App
from textual.binding import Binding
from framework.configuration import Configuration
from framework.context import ExecutionContext
from framework.eventbus import EventBus
from framework.logger import Logger
from framework.models import Environment
from framework.statistics import StatisticsCollector
from ui.controller import UIController
from ui.screens import MainScreen
class ApiTesterApp(App):
    CSS_PATH = "styles.tcss"
    TITLE = "Trade API Tester"
    #SUB_TITLE = "Enterprise API Testing Framework"
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("escape", "quit", "Exit"),
        Binding("f1", "help", "Help"),
        Binding("f2", "edit", "Edit"),
        Binding("f5", "refresh", "Refresh"),
        Binding("f9", "run_all", "Run All"),
        Binding("ctrl+f", "search", "Search"),
        Binding("ctrl+s", "save", "Save"),
        Binding("ctrl+r", "refresh", "Refresh")
    ]
    def __init__(self):
        super().__init__()
        self.execution_id = uuid.uuid4().hex[:8].upper()
        self.root_directory = Path.cwd()
        #
        # Configuration
        #
        self.configuration = Configuration(
            self.root_directory
        )
        self.configuration.load("sit")
        self.environment = Environment.model_validate(
            self.configuration.environment
        )
        #
        # Logger
        #
        self.logger = Logger(
            self.root_directory / "logs",
            self.execution_id
        ).instance
        #
        # Statistics
        #
        self.statistics = StatisticsCollector(
            self.execution_id
        )
        #
        # Context
        #
        self.context = ExecutionContext(
            execution_id=self.execution_id,
            environment=self.environment,
            configuration=self.configuration,
            logger=self.logger,
            statistics=self.statistics,
            event_bus=EventBus()
        )
        #
        # Controller
        #
        self.controller = UIController(
            self.context
        )
    # -------------------------------------------------
    def on_mount(self):
        self.title = (
            f"Trade API Tester  "
            f"| Env : SIT  "
            f"| Python : {platform.python_version()}  "
            f"| Exec : {self.execution_id}"
        )
        self.push_screen(
            MainScreen(
                controller=self.controller,
                execution_id=self.execution_id,
                environment="SIT"
            )
        )
    # -------------------------------------------------
    def action_refresh(self):
        screen = self.screen
        screen.refresh_data()
    # -------------------------------------------------
    def action_help(self):
        self.notify(
            "Help will be available in Phase 3."
        )
    # -------------------------------------------------
    def action_search(self):
        self.notify(
            "Search is not implemented yet."
        )
    # -------------------------------------------------
    def action_run_all(self):
        self.notify(
            "Run All (Phase 3)"
        )