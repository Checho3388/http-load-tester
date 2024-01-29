# http-load-tester
Just another simple HTTP tester written in python. 

## Motivation
It all started after reading the [Coding Challenges](https://codingchallenges.fyi/challenges/challenge-load-tester)
site and decided to try one of them. At the same time, I wanted to try to build the app following
the code architecture described by [Cosmic Python](https://www.cosmicpython.com/) book. 

## Installation
First, clone the repository
```shell
git clone git@github.com:Checho3388/http-load-tester.git
```

Then create the virtual environment and install the dependencies
```shell
python3 -m venv .venv
poetry install
```
You're ready to go!

## Quickstart
To run the tester, just call `ccload` inside your repository folder and add the endpoint to test.

```shell
$ ccload https://google.com
Results:
     Total Requests (2XX).......................: 1
     Failed Requests (5XX)......................: 0
     Request/second.............................: 0.85

    Total Request Time (s) (Min, Max, Mean).....: 1.01, 1.01, 1.01

```

For more options, use `-h`.

```shell
$ ccload -h
usage: ccload [-h] [-n COUNT] [-c CONCURRENCY] url

HTTP Load Tester.

positional arguments:
  url             URL to test

options:
  -h, --help      show this help message and exit
  -n COUNT        Number of tests per worker
  -c CONCURRENCY  Concurrent workers
```
