"""
Central logging utility.
"""
from __future__ import annotations
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class Logger:
    
    def __init__(
        self,
        log_directory: Path,
        execution_id: str,
        verbose: bool = False
    ):
        self._logger = logging.getLogger(f"apitester.{execution_id}")
        self._logger.setLevel(logging.DEBUG)
        self._logger.propagate = False
        if self._logger.handlers:
            return
        log_directory.mkdir(parents=True, exist_ok=True)
        log_file = log_directory / "apitest.log"
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )
        #
        # Log rotate
        #
        log_handler = RotatingFileHandler(
            log_file,
            maxBytes = 10 * 1024 * 1024,
            backupCount = 10,
            encoding = "utf-8"
        )
        self._logger.addHandler(log_handler)
        
        #
        # File Handler
        #
        # file_handler = logging.FileHandler(
            # log_file,
            # encoding="utf-8"
        # )
        # file_handler.setLevel(logging.DEBUG)
        # file_handler.setFormatter(formatter)
        # self._logger.addHandler(file_handler)
        #
        # Console Handler
        #
        # console_handler = logging.StreamHandler()
        # console_handler.setFormatter(formatter)
        # if verbose:
            # console_handler.setLevel(logging.DEBUG)
        # else:
            # console_handler.setLevel(logging.INFO)
        # self._logger.addHandler(console_handler)
    
    @property
    def instance(self) -> logging.Logger:
        return self._logger
 