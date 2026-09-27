from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Label, Button


class SearchScreen(ModalScreen):
    DEFAULT_CSS = """
    SearchScreen {
        align: center middle;
    }

    #search-dialog {
        width: 60;
        height: auto;
        padding: 2;
        border: round $accent;
        background: $surface;
    }

    #search-input {
        margin: 1 0;
    }

    #search-buttons {
        height: 3;
        align: right middle;
    }

    #search-buttons Button {
        margin-left: 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="search-dialog"):
            yield Label("Search")
            yield Input(placeholder="Enter text to search...", id="search-input")

            with Vertical(id="search-buttons"):
                yield Button("Search", id="search", variant="primary")
                yield Button("Cancel", id="cancel")

    def on_mount(self) -> None:
        self.query_one("#search-input", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search":
            value = self.query_one("#search-input", Input).value.strip()

            if not value:
                return

            self.dismiss(value)

        elif event.button.id == "cancel":
            self.dismiss(None)