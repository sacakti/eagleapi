from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label


class NewRequestScreen(ModalScreen):

    DEFAULT_CSS = """
    NewRequestScreen {
        align: center middle;
    }

    #new-request-dialog {
        width: 60;
        height: auto;
        padding: 2;
        border: round #3b82f6;
        background: $surface;
    }

    #new-request-dialog Input {
        margin-bottom: 1;
    }

    #new-request-buttons {
        height: auto;
        align: right middle;
    }

    #new-request-buttons Button {
        margin-left: 1;
    }
    """

    def compose(self):
        with Vertical(id="new-request-dialog"):
            yield Label("Create New Request")

            yield Input(
                placeholder="Request name",
                id="request-name",
            )

            yield Input(
                placeholder="HTTP method (GET, POST, PUT, DELETE...)",
                value="GET",
                id="request-method",
            )

            yield Input(
                placeholder="Request path",
                value="/",
                id="request-path",
            )

            with Vertical(id="new-request-buttons"):
                yield Button(
                    "Create",
                    id="create",
                    variant="primary",
                )
                yield Button(
                    "Cancel",
                    id="cancel",
                )

    def on_button_pressed(self, event):
        if event.button.id == "cancel":
            self.dismiss(None)
            return

        if event.button.id == "create":
            name = self.query_one(
                "#request-name",
                Input
            ).value.strip()

            method = self.query_one(
                "#request-method",
                Input
            ).value.strip().upper()

            path = self.query_one(
                "#request-path",
                Input
            ).value.strip()

            if not name:
                self.notify(
                    "Request name is required.",
                    severity="error",
                )
                return

            if not method:
                self.notify(
                    "HTTP method is required.",
                    severity="error",
                )
                return

            if not path:
                self.notify(
                    "Request path is required.",
                    severity="error",
                )
                return

            self.dismiss({
                "name": name,
                "method": method,
                "path": path,
            })