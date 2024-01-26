import dataclasses
from typing import Iterable


@dataclasses.dataclass(frozen=True)
class ProbeResult:
    elapsed_time: float
    succeeded: bool


@dataclasses.dataclass
class TestResults:
    elapsed_time: float

    total_requests: int
    failed_requests: int
    succeeded_requests: int

    throughput: float
    mean_time: float
    max_time: float
    min_time: float

    @classmethod
    def from_runner_execution(cls, elapsed_time: float, results: Iterable[ProbeResult]) -> 'TestResults':
        total = 0
        failed = 0
        total_time = 0
        min_time = 9999999999999  # Quick n' dirty
        max_time = 0

        for result in results:
            total += 1
            if not result.succeeded:
                failed += 1
            total_time += result.elapsed_time
            if min_time is None or min_time > result.elapsed_time:
                min_time = result.elapsed_time
            if max_time is None or max_time < result.elapsed_time:
                max_time = result.elapsed_time
        mean = total_time / total

        return cls(
            elapsed_time=elapsed_time,
            total_requests=total,
            failed_requests=failed,
            succeeded_requests=total-failed,
            throughput=total/elapsed_time,
            mean_time=mean,
            min_time=min_time,
            max_time=max_time
        )