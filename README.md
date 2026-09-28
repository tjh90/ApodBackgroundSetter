# ApodBackgroundSetter

Sets a desktop background to the [Astronomy Picture of the Day](https://apod.nasa.gov).

## Getting Started

## Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Running

1. Clone the repository:

    ```bash
    git clone https://github.com/tjh90/ApodBackgroundSetter.git
    cd ApodBackgroundSetter
    ```

2. Run the following from a terminal in the repo root:

    ```bash
    uv run src/ApodBackgroundSetter.py
    ```

## Testing

Tests live in [`tests/`](./tests) and use [pytest](https://docs.pytest.org). `uv run` will
create the virtual environment and install the dev dependencies on first use.

Run the full suite from the repo root:

```bash
uv run pytest -v
```

Run a single test, file, or match by expression:

```bash
uv run pytest tests/test_apod_api_request.py
uv run pytest -k GetApodImageUrlTest
```

