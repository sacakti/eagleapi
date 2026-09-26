#!/usr/bin/env python3
"""
API Tester
Entry point.
"""
from __future__ import annotations
import argparse
import sys
import uuid
from pathlib import Path

# Allow project-local libraries
env = sys.argv[1] if len(sys.argv) > 1 else "prod"

if not env == "dev":
   ROOT = Path(__file__).parent
   LIBS = ROOT / "libs"
   if LIBS.exists():
      sys.path.insert(0, str(LIBS))


from framework.configuration import Configuration
from framework.context import ExecutionContext
from framework.dashboard import Dashboard
from framework.eventbus import EventBus
from framework.loader import RequestLoader
from framework.logger import Logger
from framework.models import Environment
from framework.report import ReportGenerator
from framework.runner import Runner
from framework.scanner import EndpointScanner
from framework.statistics import StatisticsCollector
from framework.ui import ApiUI
from framework.constants import Directory

# ---------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Trade API Tester"
    )
    parser.add_argument(
        "endpoint",
        nargs="?",
        help="Endpoint folder"
    )
    parser.add_argument(
        "--request",
        help="Request file without .json"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Execute all requests"
    )
    parser.add_argument(
        "--env",
        default="sit",
        help="Environment name"
    )
    parser.add_argument(
        "--save",
        metavar="FILE",
        help="Response filename"
    )
    parser.add_argument(
        "--verbose",
        action="store_true"
    )
    return parser
# ---------------------------------------------------------
def main():
    parser = build_parser()
    args = parser.parse_args()
    root = Path.cwd()
    execution_id = uuid.uuid4().hex[:8].upper()
    #
    # UI
    #
    ui = ApiUI()
    ui.banner()
    #
    # Scanner
    #
    scanner = EndpointScanner(root)
    scanner.initialise()
    endpoints = scanner.scan()
    if not endpoints:
        ui.error(
            "No endpoints found."
        )
        return 1
    #
    # Interactive Endpoint Selection
    #
    endpoint = args.endpoint
    if endpoint is None:
        ui.show_endpoints(endpoints)
        endpoint = ui.ask(
            "Endpoint"
        )
    #
    # Configuration
    #
    configuration = Configuration(root)
    configuration.load(
        args.env
    )
    environment = Environment.model_validate(
        configuration.environment
    )
    #
    # Logger
    #
    logger = Logger(
        root / Directory.LOGS,
        execution_id,
        args.verbose
    ).instance
    #
    # Statistics
    #
    statistics = StatisticsCollector(
        execution_id
    )
    #
    # Dashboard
    #
    dashboard = Dashboard()
    dashboard.state.execution_id = execution_id
    dashboard.state.environment = args.env
    dashboard.state.endpoint = endpoint
    dashboard.start()
    #
    # Context
    #
    context = ExecutionContext(
        execution_id=execution_id,
        environment=environment,
        configuration=configuration,
        logger=logger,
        statistics=statistics,
        dashboard=dashboard,
        event_bus=EventBus()
    )
    runner = Runner(
        context
    )
    loader = RequestLoader(root)
    #
    # Execute All
    #
    if args.all:
        runner.run_all(
            endpoint,
            save_response=True
        )
    else:
        #
        # Interactive Request Selection
        #
        request_name = args.request
        if request_name is None:
            requests = loader.list_requests(
                endpoint
            )
            if not requests:
                ui.error(
                    "No requests found."
                )
                return 1
            for index, name in enumerate(
                requests,
                start=1
            ):
                ui.info(
                    f"{index}. {name}"
                )
            choice = ui.ask(
                "Request Number"
            )
            try:
                request_name = requests[
                    int(choice) - 1
                ]
            except Exception:
                ui.error(
                    "Invalid selection."
                )
                return 1
        runner.run_request(
            endpoint=endpoint,
            request_name=request_name,
            save_response=True,
            response_filename=args.save
        )
        statistics.finish()
    #
    # Summary
    #
    ui.newline()
    ui.summary(
        statistics.summary
    )
    #
    # Report
    #
    try:
        report = ReportGenerator(
            root / "framework/templates",
            root / Directory.REPORTS
        )
        report_file = report.generate(
            statistics.summary
        )
        ui.success(
            f"Report : {report_file}"
        )
    except Exception as ex:
        logger.exception(ex)
    dashboard.stop()
    return 0
# ---------------------------------------------------------
if __name__ == "__main__":
    try:
        sys.exit(
            main()
        )
    except KeyboardInterrupt:
        print()
        print("Cancelled.")
        sys.exit(130)
 