from src.domain import runner, commands
from src.domain.results import TestResults


def test_url(
        cmd: commands.TestURL,
        runner: runner.Runner,
) -> TestResults:
    """Given a URL to test, perform a group operations to get
    the number of successful attempts, throughput, mean time
    and more stats."""
    return runner.execute(
        url=cmd.url,
        count=cmd.count,
        concurrency=cmd.concurrency,
    )


COMMAND_HANDLERS = {
    commands.TestURL: test_url,
}
