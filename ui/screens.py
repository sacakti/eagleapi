"""
Main Screen
"""
from __future__ import annotations
from textual.containers import Horizontal
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer
from textual.widgets import Header
#from textual.widgets.option_list import OptionList
from textual.widgets import OptionList

from ui.widgets.endpoint_list import EndpointList
from ui.widgets.request_list import RequestList
from ui.widgets.workspace import Workspace
from ui.widgets.status import StatusBar
from ui.widgets.new_request import NewRequestScreen

class MainScreen(Screen):
    # BINDINGS = [
        # ("tab", "next_panel", "Next"),
        # ("shift+tab", "previous_panel", "Previous"),
        # ("enter", "run", "Run"),
    # ]
    BINDINGS = [
       ("tab", "next_panel", "Next"),
       ("shift+tab", "previous_panel", "Previous"),
       ("enter", "run", "Run"),
       ("ctrl+f", "search", "Search"),
       ("ctrl+n", "new", "New"),
       ("ctrl+c", "copy", "Copy"),
       ("ctrl+v", "paste", "Paste"),
       ("ctrl+s", "save", "Save"),
       ("f1", "help", "Help"),
       ("f2", "edit", "Edit"),
       ("ctrl+r", "refresh", "Refresh"),
       ("f9", "run_all", "Run All"),
       ("escape", "quit", "Exit"),
    ]

    def __init__(
        self,
        controller,
        execution_id,
        environment
    ):
        super().__init__()
        self.controller = controller
        self.execution_id = execution_id
        self.environment = environment
    # -------------------------------------------------
    def compose(self):
        yield Header(show_clock=False)
        with Vertical():
            with Horizontal(id="main-layout"):
                self.endpoint_list = EndpointList()
                self.request_list = RequestList()
                self.workspace = Workspace(
                    self.controller
                )
                yield self.endpoint_list
                yield self.request_list
                yield self.workspace
            yield StatusBar()
        yield Footer()
    # -------------------------------------------------
    def on_mount(self):
        #
        # Load Endpoints
        #
        endpoints = self.controller.load_endpoints()
        self.endpoint_list.load(
            endpoints
        )
        #
        # Load Requests
        #
        requests = self.controller.requests()
        self.request_list.load(
            requests
        )
        #
        # Preview
        #
        self.workspace.refresh_preview()
        #
        # Focus
        #
        self.set_focus(
            self.endpoint_list
        )
    # =================================================
    # Endpoint Changed
    # =================================================
    def on_option_list_option_highlighted(
        self,
        event
    ):
        #
        # Endpoint Panel
        #
        if event.option_list == self.endpoint_list:
            self.controller.select_endpoint(
                event.option_index
            )
            requests = self.controller.requests()
            self.request_list.load(
                requests
            )
            self.workspace.refresh_preview()
            return
        #
        # Request Panel
        #
        if event.option_list == self.request_list.request_list:
            self.controller.select_request(
                event.option_index
            )
            self.workspace.refresh_preview()
    # =================================================
    # TAB Navigation
    # =================================================
    def action_next_panel(self):
        focused = self.focused
        if focused == self.endpoint_list.endpoint_list:
            self.set_focus(
                self.request_list.request_list
            )
        elif focused == self.request_list.request_list:
            self.set_focus(
                self.workspace
            )
        elif focused == self.request_list.run_all_button:
            self.set_focus(
                self.workspace
            )
    # -------------------------------------------------
    def action_previous_panel(self):
        focused = self.focused
        if focused == self.workspace:
            self.set_focus(
                self.request_list.request_list
            )
        elif focused == self.request_list.request_list:
            self.set_focus(
                self.endpoint_list
            )
        elif focused == self.request_list.run_all_button:
            self.set_focus(
                self.request_list.request_list
            )
        else:
            self.set_focus(
                self.workspace
            )
    # # =================================================
    # # ENTER
    # # =================================================
    # def action_run(self):
        # #
        # # Endpoint
        # #
        # if self.focused == self.endpoint_list:
            # self.workspace.show_execution()
            # self.workspace.clear_execution()
            # self.workspace.execution(
                # f"Running endpoint : "
                # f"{self.controller.endpoint.name}"
            # )
            # self.controller.run_current_endpoint()
            # return
        # #
        # # Request
        # #
        # # if self.focused == self.request_list:
            # # #
            # # # Run All
            # # #
            # # if self.request_list.run_all_selected:
                # # self.workspace.show_execution()
                # # self.workspace.clear_execution()
                # # self.workspace.execution(
                    # # "Running all requests..."
                # # )
                # # self.controller.run_current_endpoint()
                # # return
            # # #
            # # # Single
            # # #
            # # self.workspace.show_execution()
            # # self.workspace.clear_execution()
            # # self.workspace.execution(
                # # f"Running "
                # # f"{self.controller.request}"
            # # )
            # # result = self.controller.run_current_request()
            # # self.workspace.execution(
                # # "Completed"
            # # )
            # # #
            # # # TODO
            # # # Populate Response Tab
            # # #
        
        # if self.focused == self.request_list:
           # #
           # # Run All
           # #
           # if self.request_list.run_all_selected:
               # self.workspace.show_execution()
               # self.workspace.clear_execution()
               # self.workspace.execution(
                   # "Running all requests...\n"
               # )
               # results = self.controller.run_current_endpoint()
               # self.workspace.execution(
                   # f"\nCompleted : {len(results)} request(s)"
               # )
               # return
           # #
           # # Single Request
           # #
           # # self.workspace.show_execution()
           # # self.workspace.clear_execution()
           # # self.workspace.execution("Connecting...\n")
           # result = self.controller.run_current_request()
           # if result:
               # self.workspace.show_execution_result(result)
           # # self.workspace.execution(
               # # f"HTTP {result.http_status}\n"
           # # )
           # # self.workspace.execution(
               # # f"{result.response_time_ms:.2f} ms\n"
           # # )
           # # self.workspace.execution(
               # # f"{result.response_size:,} Bytes\n"
           # # )
           # # self.workspace.execution(
               # # "Saved Response\n"
           # # )
           # # self.workspace.response(
               # # result.response_body
           # # )

    def on_option_list_option_selected(
       self,
       event: OptionList.OptionSelected,
    ):
        #
        # Endpoint
        #
        if event.option_list is self.endpoint_list.endpoint_list:
            self.workspace.show_execution()
            self.workspace.clear_execution()
            results = self.controller.run_current_endpoint()
            self.workspace.execution(
                f"Completed {len(results)} request(s)"
            )
            return
        #
        # Request
        #
        if event.option_list is self.request_list.request_list:
            self.workspace.show_execution()
            self.workspace.clear_execution()

            result = self.controller.run_current_request()

            if result is not None:
                self.workspace.show_execution_result(
                    result
                )
    
    def on_button_pressed(
        self,
        event: Button.Pressed,
    ):
        if event.button.id == "run-all-endpoints":
            self.workspace.show_execution()
            self.workspace.clear_execution()

            results = self.controller.run_all_endpoints()

            self.workspace.execution(
                f"Completed {len(results)} endpoint(s)"
            )

            return

        if event.button.id == "run-all-requests":
            self.workspace.show_execution()
            self.workspace.clear_execution()

            results = self.controller.run_current_endpoint()

            self.workspace.execution(
                f"Completed {len(results)} request(s)"
            )
    
    def action_edit(self):
        self.workspace.enable_edit()

        self.notify(
            "Edit mode enabled. Press Ctrl+S to save."
        )

    def action_save(self):
        if not self.workspace.is_editing():
            self.notify(
                "Edit mode is not enabled."
            )
            return

        try:
            self.controller.save_current_request(
                self.workspace.preview_text()
            )

            self.workspace.disable_edit()

            self.workspace.refresh_preview()

            self.notify(
                "Request saved successfully."
            )

        except Exception as exc:
            self.notify(
                f"Save failed: {exc}",
                severity="error"
            )
    def action_refresh(self):
        self.endpoint_list.load(
            self.controller.load_endpoints()
        )

        self.request_list.load(
            self.controller.requests()
        )

        self.workspace.refresh_preview()

        self.notify("Refreshed")

    def action_new(self):
        def handle_new_request(data):
            if data is None:
                return

            try:
                self.controller.create_request(
                    name=data["name"],
                    method=data["method"],
                    path=data["path"],
                )

                # Reload request list
                requests = self.controller.requests()

                self.request_list.load(
                    requests
                )

                # Select newly created request
                for index, request_name in enumerate(requests):
                    if request_name == data["name"]:
                        self.request_list.request_list.highlighted = index
                        self.controller.select_request(index)
                        break

                # Refresh preview
                self.workspace.refresh_preview()

                self.notify(
                    f"Request '{data['name']}' created."
                )

            except Exception as exc:
                self.notify(
                    f"Create failed: {exc}",
                    severity="error",
                )

        self.app.push_screen(
            NewRequestScreen(),
            handle_new_request,
        )