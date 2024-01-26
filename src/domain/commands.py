import dataclasses


@dataclasses.dataclass
class TestURL:
    url: str
    count: int
    concurrency: int
