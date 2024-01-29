import abc
from typing import Iterator

import requests

from ..domain.results import ProbeResult


class AbstractClient(abc.ABC):
    @abc.abstractmethod
    def test(self, url: str) -> Iterator[ProbeResult]:
        """Main client method, in charge of
        testing the URL and returning the response
        object."""


class RequestsClient(AbstractClient):
    """Simple client using python requests library"""
    def test(self, url: str) -> ProbeResult:
        response = requests.get(url)
        return ProbeResult(
            elapsed_time=response.elapsed.total_seconds(),
            succeeded=response.ok,
        )
