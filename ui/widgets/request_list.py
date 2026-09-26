"""
Request List Widget
"""

from textual.containers import Vertical
from textual.widgets import Button, OptionList


class RequestList(Vertical):

    DEFAULT_CSS = """
    RequestList {
        height: 100%;
        width: 100%;
    }

    RequestList > #request-list {
        height: 1fr;
    }

    RequestList > #run-all-requests {
        height: 3;
        width: 100%;
    }
    """

    RUN_ALL_TEXT = "▶ Run All Requests"

    def __init__(self):
        super().__init__()
        self._requests = []

        self.request_list = OptionList(
            id="request-list"
        )

        self.run_all_button = Button(
            self.RUN_ALL_TEXT,
            id="run-all-requests",
            variant="primary",
        )

    def compose(self):
        yield self.request_list
        yield self.run_all_button

    # --------------------------------------------------
    # Load Requests
    # --------------------------------------------------

    def load(self, requests):
        """
        requests:
            List[RequestDefinition]
        """

        self.request_list.clear_options()

        self._requests = list(requests)

        for request in self._requests:
            self.request_list.add_option(
                f"{request}"
            )

        if self.request_list.option_count:
            self.request_list.highlighted = 0

    # --------------------------------------------------
    # Selected Request
    # --------------------------------------------------

    @property
    def highlighted(self):
        return self.request_list.highlighted

    @property
    def selected_request(self):
        index = self.request_list.highlighted

        if index is None:
            return None

        if index < 0 or index >= len(self._requests):
            return None

        return self._requests[index]

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def current_name(self):
        request = self.selected_request

        if request is None:
            return None

        return request.name

    def current_request(self):
        return self.selected_request

    def current_method(self):
        return None

    def current_path(self):
        return None

    def has_requests(self):
        return len(self._requests) > 0