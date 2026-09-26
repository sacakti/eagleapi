"""
Endpoint List Widget
"""

from textual.containers import Vertical
from textual.widgets import Button, OptionList


class EndpointList(Vertical):

    DEFAULT_CSS = """
    EndpointList {
        height: 100%;
        width: 100%;
    }

    EndpointList > #endpoint-list {
        height: 1fr;
    }

    EndpointList > #run-all-endpoints {
        height: 3;
        width: 100%;
    }
    """

    def __init__(self):
        super().__init__()

        self._endpoints = []

        self.endpoint_list = OptionList(
            id="endpoint-list"
        )

        self.run_all_button = Button(
            "▶ Run All Endpoints",
            id="run-all-endpoints",
            variant="primary",
        )

    def compose(self):
        yield self.endpoint_list
        yield self.run_all_button

    # --------------------------------------------------
    # Load Endpoints
    # --------------------------------------------------

    def load(self, endpoints):
        """
        endpoints:
            List[EndpointDefinition]
        """

        self.endpoint_list.clear_options()

        self._endpoints = list(endpoints)

        for endpoint in self._endpoints:
            self.endpoint_list.add_option(
                f"📁 {endpoint.name} ({endpoint.request_count})"
            )

        if self.endpoint_list.option_count:
            self.endpoint_list.highlighted = 0

    # --------------------------------------------------
    # Selected Endpoint
    # --------------------------------------------------

    @property
    def highlighted(self):
        return self.endpoint_list.highlighted

    @property
    def selected_endpoint(self):
        if (
            self.endpoint_list.highlighted is None
            or self.endpoint_list.highlighted < 0
            or self.endpoint_list.highlighted >= len(self._endpoints)
        ):
            return None

        return self._endpoints[self.endpoint_list.highlighted]

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def current_name(self):
        endpoint = self.selected_endpoint

        if endpoint is None:
            return None

        return endpoint.name

    def current_path(self):
        endpoint = self.selected_endpoint

        if endpoint is None:
            return None

        return endpoint.path