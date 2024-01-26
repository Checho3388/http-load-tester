import argparse

from src import bootstrap
from src.domain import commands
from src.adapters import formatter

app = bootstrap.bootstrap()


def test_url(url: str, count: int, concurrency: int):
    cmd = commands.TestURL(url=url, count=count, concurrency=concurrency)
    results = app.handle(cmd)
    print(formatter.string_summary(results))


def main():  # pragma no cover
    parser = argparse.ArgumentParser(description='HTTP Load Tester.')
    parser.add_argument('url', help='URL to test', type=str)
    parser.add_argument('-n', dest='count', type=int, default=1, help='Number of tests per worker')
    parser.add_argument('-c', dest='concurrency', type=int, default=1, help='Concurrent workers')

    args = parser.parse_args()
    test_url(url=args.url, count=args.count, concurrency=args.concurrency)


if __name__ == "__main__":  # pragma no cover
    main()
