# Copilot Instructions for dltreader

## Project Overview
- **Purpose:** Python module for reading AUTOSAR DLT (Diagnostic, Log and Trace) files and streams, focusing on pure Python, minimal dependencies, and permissive licensing.
- **Main Features:**
  - Read `.dlt` files and parse DLT messages (standard, extended headers, payloads)
  - Support for both file-based and TCP stream-based DLT sources
  - Handles both verbose and non-verbose payloads, with extensible type system
  - Includes CLI tools for analysis, statistics, and plotting

## Key Components
- **dlt/**: Core library
  - `reader.py` / `receiver.py` / `async_receiver.py`: File, TCP, and async TCP DLT readers (context managers, iterable)
  - `header/`, `payload/`, `types/`: Parsers for DLT headers, payloads, and argument types
  - `packet.py`: Combines headers and payloads into packets
  - `constants.py`: DLT protocol enums and bitmasks
  - `services/`: DLT control message service classes
- **Scripts:**
  - `test.py`, `test_dlt.py`, `test_dlt2.py`: Example/test scripts for file and network reading
  - `dlt_analyzer.py`, `dlt_volume.py`, `lf_stat.py`, `compact_reader.py`: CLI tools for analysis, statistics, and data extraction

## Usage Patterns
- **Basic file reading:**
  ```python
  from dlt import DltReader
  with DltReader("example.dlt") as r:
      for storage_header, packet in r:
          if packet.has_payload():
              print(packet)
  ```
- **TCP stream reading:**
  ```python
  from dlt import DltReceiver
  with DltReceiver(host, port) as r:
      for _, packet in r:
          ...
  ```
- **Async TCP reading:**
  ```python
  from dlt import DltAsyncReceiver
  async with DltAsyncReceiver(host, port) as r:
      async for _, packet in r:
          ...
  ```

## Developer Workflows
- **Install:** `pip install -U dltreader` (see README)
- **Test/Run:** Use scripts in root directory; e.g. `python test.py` or `python dlt_analyzer.py --path_log file.dlt`
- **Docs:** Build with `cd docs && mkdocs build` (requires `mkdocs`)
- **Debug:** Use VSCode launch config or run scripts directly

## Project Conventions
- **No external dependencies** (except optional `mkdocs` for docs, `plotly` for analysis, `deepdiff` for compact_reader)
- **Type system:** New DLT payload types should subclass `DltPayloadArgumentBaseType` and register in `dlt/types/__init__.py` and `payloadverbose.py` mapping
- **Error handling:** Most parsing errors are logged and skipped, not raised
- **Partial AUTOSAR DLT support:** Only a subset of the protocol is implemented; see `docs/background.md` for protocol details
- **No write support:** Only reading/parsing is implemented

## Integration Points
- **External:**
  - Consumes `.dlt` files or TCP DLT streams (AUTOSAR standard)
  - No direct integration with other systems
- **Extending:**
  - Add new payload types in `dlt/types/`
  - Add new service handlers in `dlt/services/`

## References
- See `README.rst` and `docs/` for user-facing documentation and protocol background
- Example usage: `docs/docs/usage.md`
- Protocol details: `docs/docs/background.md`

---

**When contributing code, follow the patterns in `dlt/` and reference the CLI scripts for real-world usage.**
