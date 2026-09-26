"""
Response validation engine.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from framework.models import (
   Assertion,
   ResponseDefinition,
)

@dataclass
class ValidationMessage:
    name: str
    success: bool
    expected: str
    actual: str
    message: str

@dataclass
class ValidationResult:
    passed: bool = True
    messages: List[ValidationMessage] = field(
        default_factory=list
    )
    def add(self, message: ValidationMessage):
        self.messages.append(message)
        if not message.success:
            self.passed = False

class Validator:
    def validate(
        self,
        assertion: Assertion,
        response: ResponseDefinition
    ) -> ValidationResult:
        result = ValidationResult()
        if assertion is None:
            return result
        #
        # Status Code
        #
        if assertion.status is not None:
            success = (
                response.status_code ==
                assertion.status
            )
            result.add(
                ValidationMessage(
                    name="HTTP Status",
                    success=success,
                    expected=str(assertion.status),
                    actual=str(response.status_code),
                    message="Status code validation"
                )
            )
        #
        # Response Time
        #
        if assertion.response_time is not None:
            success = (
                response.elapsed_ms <=
                assertion.response_time
            )
            result.add(
                ValidationMessage(
                    name="Response Time",
                    success=success,
                    expected=f"<= {assertion.response_time} ms",
                    actual=f"{response.elapsed_ms:.2f} ms",
                    message="Response time validation"
                )
            )
        #
        # Headers
        #
        for key, expected in assertion.headers.items():
            actual = response.headers.get(key)
            success = (
                str(actual) ==
                str(expected)
            )
            result.add(
                ValidationMessage(
                    name=f"Header [{key}]",
                    success=success,
                    expected=str(expected),
                    actual=str(actual),
                    message="Header validation"
                )
            )
        #
        # JSON Validation
        #
        if (
            assertion.json and
            isinstance(response.body, dict)
        ):
            for key, expected in assertion.json.items():
                actual = response.body.get(key)
                success = (
                    actual ==
                    expected
                )
                result.add(
                    ValidationMessage(
                        name=f"JSON [{key}]",
                        success=success,
                        expected=str(expected),
                        actual=str(actual),
                        message="JSON validation"
                    )
                )
        #
        # Body Contains
        #
        if assertion.body_contains:
            body = str(response.body)
            success = (
                assertion.body_contains
                in body
            )
            result.add(
                ValidationMessage(
                    name="Body Contains",
                    success=success,
                    expected=assertion.body_contains,
                    actual="Found"
                    if success
                    else "Not Found",
                    message="Body content validation"
                )
            )
        return result