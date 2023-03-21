# Welcome to dlt

The Python `dlt` module provides an easy way to read `.dlt` files that are
based on the AUTOSAR "Diagnostic, Log and Trace Protocol Specification" format.
It has no other dependencies and just relies on the Python.


## Disclaimer

The implementation of this module is just a proof-of-concept and covers only a
subset of the entire standard; besides, it is only partially tested, so do not
use this in production! The focus of this module is currently only on the
reading of `.dlt` files, without considering any writing functionality. Apart
from this, the focus of this implementation is to just make it work, i.e.,
performance optimizations, e.g., when reading the file are, are currently
out of scope.
