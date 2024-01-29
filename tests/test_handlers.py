from src import bootstrap
from src.adapters import client
from src.domain import commands
from src.domain.results import ProbeResult
from src.domain.runner import Runner, FakeFixedClock


class FakeClient(client.AbstractClient):
    def __init__(self, succeeded: bool = True):
        self._registry = []
        self._succeeded = succeeded

    def test(self, url: str) -> ProbeResult:
        self._registry.append(url)
        return ProbeResult(
            elapsed_time=1,
            succeeded=self._succeeded
        )

    def assert_tested(self, url):
        assert url in self._registry


class FakeAletrnatingClient(client.AbstractClient):
    def __init__(self, results: list[ProbeResult]):
        self._registry = []
        self._results = results

    def test(self, url: str) -> ProbeResult:
        self._registry.append(url)
        return self._results.pop()

    def assert_tested(self, url):
        assert url in self._registry


def bootstrap_test_app(client_factory):
    return bootstrap.bootstrap(
        runner=Runner(
            execution_clock=FakeFixedClock,
            client_factory=client_factory
        )
    )


def test_url_test_success():
    app = bootstrap_test_app(FakeClient())
    results = app.handle(command=commands.TestURL("sarasa", 1, 1))
    assert results.succeeded_requests == 1
    assert results.failed_requests == 0
    assert results.total_requests == 1


def test_url_test_fail():
    app = bootstrap_test_app(FakeClient(succeeded=False))
    results = app.handle(command=commands.TestURL("sarasa", 1, 1))
    assert results.succeeded_requests == 0
    assert results.failed_requests == 1
    assert results.total_requests == 1


def test_url_test_success_then_fail_repeat():
    app = bootstrap_test_app(
        FakeAletrnatingClient(
            [ProbeResult(1, True), ProbeResult(1, False)]
        )
    )
    results = app.handle(command=commands.TestURL("sarasa", 2, 1))
    assert results.succeeded_requests == 1
    assert results.failed_requests == 1
    assert results.total_requests == 2


def test_url_test_success_then_fail_concurrent():
    app = bootstrap_test_app(
        FakeAletrnatingClient(
            [ProbeResult(1, True), ProbeResult(1, False)]
        )
    )
    results = app.handle(command=commands.TestURL("sarasa", 1, 2))
    assert results.succeeded_requests == 1
    assert results.failed_requests == 1
    assert results.total_requests == 2

#
# def when_the_runner_checks_the_url(url, count, concurrency):
#     return Runner(
#         execution_clock=FakeFixedClock,
#         client_factory=fake_probe_factory()
#     ).execute(url, count, concurrency)
#
#
# def summary_is_all_200(execution_results):
#     assert execution_results == TestResults(
#         elapsed_time=1,
#         mean_time=1.0,
#         max_time=1,
#         total_requests=1,
#         succeeded_requests=1,
#         failed_requests=0,
#         min_time=1,
#         throughput=1,
#     )
#
#
# def then_runner_results_are_as_expected(execution_results):
#     assert execution_results == TestResults(
#         elapsed_time=1,
#         mean_time=1.5,
#         max_time=2.0,
#         total_requests=2,
#         succeeded_requests=1,
#         failed_requests=1,
#         min_time=1,
#         throughput=2.0,
#     )
#
#
# def then_string_summary_is(summary: str):
#     assert summary == """Results:
#      Total Requests (2XX).......................: 1
#      Failed Requests (5XX)......................: 0
#      Request/second.............................: 1
#
#     Total Request Time (s) (Min, Max, Mean).....: 1.0, 1.00, 1.00"""
#
#
# def test_1():
#     results = when_the_runner_checks_the_url(
#         url="sarasa",
#         count=1,
#         concurrency=1,
#     )
#     summary_is_all_200(results)

