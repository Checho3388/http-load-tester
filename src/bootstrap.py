import inspect

from src.domain import runner
from src.service_layer import app, handlers


def bootstrap(
    runner: runner.Runner = runner.Runner(),
) -> app.App:
    dependencies = {"runner": runner}

    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return app.App(
        runner=runner,
        formatter=None,
        command_handlers=injected_command_handlers,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
