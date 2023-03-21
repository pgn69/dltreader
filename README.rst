Read Me
=======

The `dltreader` Python module allows the reading of AUTOSAR
["Diagnostic, Log and Trace Protocol"](https://www.autosar.org/fileadmin/standards/foundation/1-0/AUTOSAR_PRS_DiagnosticLogAndTraceProtocol.pdf) files.
files.


Why?
----

The goal of this module is to provide a simple, purely Python-based module to
read `.dlt` files without further dependencies. Apart from that a permissive
free software license shall is supported to make it usable in possible
commercial contexts.


Example
-------




Limitations
-----------

At current point in time the module is a PoC so should not be used in
production software; besides, it is only a partial implementation of the
overall standard and not optimized for performance.


Docs
----

Please check the `docs/` directory for further details.


Related DLT projects
--------------------

Python modules for DLT (without claim to be complete):

* https://pypi.org/project/dltpy (requires C++ dependencies)
* https://github.com/r2b1d1/dlt2json (converts DLT to json format)
* https://gitlab.com/Menschel/logging-dlt (similar but using GPL)
* https://pypi.org/project/pydlt (provides also writing of DLT messages)
* ...

Similar projects in other programming languages:

* https://github.com/esrlabs/dlt-reader/
* https://github.com/COVESA/dlt-daemon/
* ...
