"""
HTML report generator.
"""
from __future__ import annotations
import html
from datetime import datetime
from pathlib import Path
from typing import List
from jinja2 import Environment, FileSystemLoader
from framework.models import (
   ExecutionResult,
   Statistics,
)

class ReportGenerator:
    def __init__(
        self,
        template_directory: Path,
        output_directory: Path
    ):
        self._environment = Environment(
            loader=FileSystemLoader(
                str(template_directory)
            ),
            autoescape=True
        )
        self._output_directory = output_directory
    # --------------------------------------------------
    def generate(
        self,
        statistics: Statistics
    ) -> Path:
        template = self._environment.get_template(
            "report.html"
        )
        report_name = (
            f"{statistics.execution_id}.html"
        )
        output = (
            self._output_directory /
            report_name
        )
        html_content = template.render(
            generated=datetime.now(),
            statistics=statistics,
            results=statistics.results
        )
        output.write_text(
            html_content,
            encoding="utf-8"
        )
        return output