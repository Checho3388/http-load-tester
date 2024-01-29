import collections
import concurrent.futures
import time
from typing import Iterator

from src.adapters import client
from src.domain.results import TestResults


class Clock:
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._elapsed = time.time() - self.start_time

    @property
    def elapsed(self) -> float:
        return self._elapsed


class FakeFixedClock:
    def __init__(self, duration: float = 1):
        self.duration = duration

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._elapsed = self.duration

    @property
    def elapsed(self) -> float:
        return self._elapsed


class Runner:
    def __init__(self, client_factory=client.RequestsClient(), execution_clock=Clock):
        self.execution_clock = execution_clock
        self.collector_factory = collections.deque
        self.client = client_factory

    def execute(self, url: str, count: int, concurrency: int) -> TestResults:
        collector = self.collector_factory(maxlen=count*concurrency)
        with self.execution_clock() as clock:
            collector.extend(
                self.run_n_times_in_m_workers(
                    url=url,
                    count=count,
                    concurrency=concurrency
                )
            )

        return TestResults.from_runner_execution(
            elapsed_time=clock.elapsed,
            results=collector,
        )

    def run_n_times(self, url: str, count: int) -> Iterator[client.ProbeResult]:
        for i in range(count):
            yield self.client.test(url=url)

    def run_n_times_in_m_workers(self, url: str, count: int, concurrency: int) -> Iterator[client.ProbeResult]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            fn = [
                executor.submit(self.run_n_times, url, count) for _ in range(concurrency)
            ]
            for future in concurrent.futures.as_completed(fn):
                for result in future.result():
                    yield result
