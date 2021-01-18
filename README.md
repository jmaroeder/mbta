# mbta

Command-line utility to find the next departing train for a particular stop on the MBTA T network.

## Quick-start (no installation)

If you have [Docker](https://www.docker.com/), you can run without installing anything else:

```shell
$ docker run --rm -it jmaroeder/mbta
```

## Installation

### Prerequisites

Make sure you have the following prerequisites installed:

- [poetry](https://python-poetry.org/)
- [Python 3.8](https://www.python.org/)

### Clone Git Repo

```shell
$ git clone https://github.com/jmaroeder/mbta.git
$ cd mbta
$ poetry install
```

## Usage

```shell
$ mbta --help
```

## Tests

Run tests via `pytest`:

```shell
$ pytest
```
