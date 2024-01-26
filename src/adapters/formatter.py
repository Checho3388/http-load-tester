import dataclasses
import json

from ..domain.results import TestResults


def string_summary(results: TestResults) -> str:
    """Returns a string summary of the test results just like the
    cli would print to the terminal."""
    return f"""Results:
     Total Requests (2XX).......................: {results.total_requests}
     Failed Requests (5XX)......................: {results.failed_requests}
     Request/second.............................: {results.throughput:.2f}

    Total Request Time (s) (Min, Max, Mean).....: {results.min_time:.2f}, {results.max_time:.2f}, {results.mean_time:.2f}
    """
