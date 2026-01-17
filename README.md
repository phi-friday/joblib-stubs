# joblib-stubs

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/joblib-stubs.svg)](https://badge.fury.io/py/joblib-stubs)
[![python version](https://img.shields.io/pypi/pyversions/joblib-stubs.svg)](#)

Type stubs for the [joblib](https://github.com/joblib/joblib) library.

> [!NOTE]  
> This package provides type hints only and contains no runtime code.  
> For the actual runtime implementation, install [`joblib`](https://github.com/joblib/joblib).

> [!WARNING]  
> This package does **not** include type stubs for `joblib.externals` (bundled `cloudpickle` and `loky`).

## Installation

```shell
pip install joblib-stubs
```

## Usage

Once installed, type checkers will automatically discover and use these stubs when analyzing code that uses `joblib`:

```python
from math import sqrt
from typing import assert_type

from joblib import Parallel, delayed

# Your type checker will now understand joblib's types
results = Parallel(n_jobs=2)(delayed(sqrt)(i**2) for i in range(10))
assert_type(results, list[float])
```

## License

MIT - see [LICENSE](https://github.com/phi-friday/joblib-stubs/blob/main/LICENSE) for details.
