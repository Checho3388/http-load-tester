from typing import Callable

from src.domain import runner


class App:
    def __init__(
        self,
        runner: runner.Runner(),
        formatter: Callable,
        command_handlers: dict[str, Callable],
    ):
        self.runner = runner
        self.formatter = formatter
        self.command_handlers = command_handlers

    def handle(self, command):
        handler = self.command_handlers[type(command)]
        return handler(command)
