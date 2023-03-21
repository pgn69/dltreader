# Usage

Just open the file and iterate over the reader to obtain the packets:

```
from dlt import DltReader
from dlt.payload import DltPayloadNonVerbose, DltPayloadVerbose


with DltReader("example.dlt") as r:
    for storage_header, packet in r:
        if not packet.has_payload():
            # skip packets that do not have a payload
            continue

        if isinstance(packet.payload, DltPayloadNonVerbose):
            # non-verbose payload
            print("non-verbose", packet)

        elif isinstance(packet.payload, DltPayloadVerbose):
            # verbose payload
            print("verbose", packet)
```
