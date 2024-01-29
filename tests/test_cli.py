from src.entrypoints import cli
import requests_mock


def test_cli(capsys):
    with requests_mock.Mocker() as m:
        m.get('http://test.com')
        cli.test_url('http://test.com', 1, 1)

    captured = capsys.readouterr()
    result = captured.out

    assert "Total Requests (2XX).......................: 1" in result
    assert "Failed Requests (5XX)......................: 0" in result
    assert "Request/second.............................: " in result
    assert "Total Request Time (s) (Min, Max, Mean).....: " in result
