from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Label, Button


class EnvironmentScreen(ModalScreen):
    DEFAULT_CSS = """
    EnvironmentScreen {
        align: center middle;
    }

    #environment-dialog {
        width: 70;
        height: auto;
        padding: 2;
        border: round $accent;
        background: $surface;
    }

    #base-url {
        margin: 1 0;
    }

    #environment-buttons {
        height: 3;
        align: right middle;
    }

    #environment-buttons Button {
        margin-left: 1;
    }
    """

    def __init__(self, environment_name: str, base_url: str):
        super().__init__()
        self.environment_name = environment_name
        self.base_url = base_url

    def compose(self) -> ComposeResult:
        with Vertical(id="environment-dialog"):
            yield Label(
                f"Environment: {self.environment_name}"
            )

            yield Label("Base URL")

            yield Input(
                value=self.base_url,
                id="base-url",
            )

            with Vertical(id="environment-buttons"):
                yield Button(
                    "Save",
                    id="save",
                    variant="primary",
                )
                yield Button(
                    "Cancel",
                    id="cancel",
                )

    def on_mount(self) -> None:
        self.query_one("#base-url", Input).focus()

    def on_button_pressed(
        self,
        event: Button.Pressed,
    ) -> None:

        if event.button.id == "save":

            base_url = self.query_one(
                "#base-url",
                Input,
            ).value.strip()

            if not base_url:
                return

            self.dismiss(base_url)

        elif event.button.id == "cancel":
            self.dismiss(None)