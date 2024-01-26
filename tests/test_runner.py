from src.adapters import client
from src.domain.results import ProbeResult
from src.domain.runner import Runner


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
        assert url in self._registry, \
            f"Expected to found {url} in {[url for url in self._registry]}"


def test_runner_respects_requests_count():
    runner = Runner(
        client_factory=FakeClient(),
    )
    results = runner.run_n_times("sarasa", 10)

    assert len([r for r in results]) == 10


def test_runner_checks_for_given_url():
    client = FakeClient()
    runner = Runner(
        client_factory=client,
    )
    runner.execute("sarasa", 1, 1)
    client.assert_tested("sarasa")


def test_runner_works_with_concurrency():
    client = FakeClient()
    runner = Runner(
        client_factory=client,
    )

    results = runner.run_n_times_in_m_workers("sarasa", 1, 10)

    assert len([r for r in results]) == 10
    client.assert_tested("sarasa")
