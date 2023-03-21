# Background

The AUTOSAR "Diagnostic, Log and Trace Protocol Specification" package format,
in short DLT, is specified in [AUTOSAR_PRS_DiagnosticLogAndTraceProtocol.pdf](https://www.autosar.org/fileadmin/standards/foundation/1-0/AUTOSAR_PRS_DiagnosticLogAndTraceProtocol.pdf).

The basic structure in a nutshell is discussed in the following:


## Storage Header

The storage header will be placed before each DLT message in a stored file:

```
| DLT-Pattern |       Timestamp        | ECU ID | DLT message |
|             | seconds | milliseconds |        |             |
```

The corresponding byte positions and data types are as follows:

| Byte | Description                | Data Type |
|------|----------------------------|-----------|
|  0   | DLT-Pattern ("DLT" + 0x01) |  char[4]  |
|  4   | Timestamp                  |           |
|      | -> 4-7: seconds            |  uint32   |
|      | -> 8-11 milliseconds)      |  uint32   |
|  12  | ECU ID                     |  char[4]  |
|  16  | DLT Message (header+extended header+payload) |     [...]     |


## Dlt Message Format

After the storage header the DLT message will follow:

```
| Standard |  Extended |              Payload              |
| Header   |  Header   |                                   |
```

The standard header must always be there, while the extended header is only
available if the UEH bit in the HTYP field is set (see below). The last part
of the package is the payload that carries the actual data, but can also be
empty.


## Header Format

In the following the header formats are discussed in depth:

### Standard Header

The most important header is the standard header that consists of the following
fields:

```
| HTYP | MCNT | LEN |   ECU   |    SEID   |    TMSP     |
|  0   |  1   | 2 3 | 4 5 6 7 | 8 9 10 11 | 12 13 14 15 |
```

| Byte | Description                  | Data Type |
|------|------------------------------|-----------|
|    0 | HTYP  (Header Type)          | byte      |
|    1 | MCNT  (Message Counter)      | uint8     |
| 2- 3 | LEN   (Length)               | uint16    |
| 4- 7 | ECU   (ECU ID, optional)     | char[4]   |
| 8-11 | SEID  (Session ID, optional) | uint32    |
|12-15 | TMSP  (Timestamp, optional)  | uint32    |

*notice*: `LEN` describes the overall length of the DLT message, i.e., including:

* standard header
* optional extended header
* optional payload


#### HTYP

The header type `HTYP` consists of the following bits:

| Bit | Description                                         |
|-----|-----------------------------------------------------|
|  0  | UEH  (Use Extended Header)                          |
|  1  | MSBF (Most significat byte first, i.e., big endian) |
|  2  | WEID (with ECU ID)                                  |
|  3  | WSID (with Session ID)                              |
|  4  | WTMS (with Timestamp)                               |
|  57 | VERS (Version number)                               |


### Extended Header

The extended header is only presen, if the `UEH` bit is set in the `HTYP`
byte of the standard header.

```
| MSIN |  NOAR |  APID    |  CTID   |
|  0   |   1   | 2 3 4 5  | 6 7 8 9 |
```

| Byte | Description                  | Data Type |
|------|------------------------------|-----------|
|   0  | MSIN   (Message Info)        | byte      |
|   1  | NOAR   (Number of Arguments) | uint8     |
| 2-5  | APID   (Application ID)      | char[4]   |
| 6-9  | CTID   (Context ID)          | char[4]   |

The invidiual extended header fields are discussed in the following:

#### MSIN

| Bit | Description                   |
|-----|-------------------------------|
|   0 | VERB  (Use Verbose Mode)      |
| 1-3 | MSTP  (Message Type)          |
| 4-7 | MSTIN (Message Type Info)     |


##### MSTP and corresponding MSTIN

| MSTP Value | MSIN Value | Description                                       |
|------------|------------|---------------------------------------------------|
|    0x0     |            | Dlt_TYPE_LOG           (Dlt Log Message)          |
|            |    0x1     | DLT_LOG_FATAL          (Fatal system error)       |
|            |    0x2     | DLT_LOG_ERROR          (SWC error)                |
|            |    0x3     | DLT_LOG_WARN           (Correct behavior not sure)|
|            |    0x4     | DLT_LOG_INFO           (LogLevel type "Info")     |
|            |    0x5     | DLT_LOG_DEBUG          (LogLevel type "Debug")    |
|            |    0x6     | DLT_LOG_VERBOSE        (LogLevel type "Verbose")  |
|    0x1     |            | Dlt_TYPE_APP_TRACE     (Dlt Trace Message)        |
|            |    0x1     | DLT_TRACE_VARIABLE     (Value of variable)        |
|            |    0x2     | DLT_TRACE_FUNCTION_IN  (Call of a function)       |
|            |    0x3     | DLT_TRACE_FUNCTION_OUT (Return of a function)     |
|            |    0x4     | DLT_TRACE_STATE        (State of a State Machine) |
|            |    0x5     | DLT_TRACE_VFB          (RTE events)               |
|    0x2     |            | Dlt_TYPE_NW_TRACE     (Dlt Network Message)       |
|            |    0x1     | DLT_NW_TRACE_IPC      (IPC)                       |
|            |    0x2     | DLT_NW_TRACE_CAN      (CAN Communications bus)    |
|            |    0x3     | DLT_NW_TRACE_FLEXRAY  (FlexRay Communications bus)|
|            |    0x4     | DLT_NW_TRACE_MOST     (Most Communications bus)   |
|            |    0x5     | DLT_NW_TRACE_ETHERNET (Eth Communications bus)    |
|            |    0x6     | DLT_NW_TRACE_SOMEIP   (SOME/IP Communication)     |
|            |  0x7-0x15  | User Defined          (User defined settings      |
|    0x3     |            | Dlt_TYPE_CONTROL      (Dlt Control Message)       |
|            |    0x1     | DLT_CONTROL_REQUEST   (Request Control Message)   |
|            |    0x2     | DLT_CONTROL_RESPONSE  (Respond Control Message)   |
| 0x4– 0x15  |            | Reserved                                          |


## Payload

There are two different types of payload:

### non-verbose mode

For parameter values without metadata information.

```
Standard |           Payload            |
Header   | Message ID | non-static data |
```

Message ID: uint32


### verbose-mode

For a complete description of the parameters next to the parameter values.

```
Standard | Extended |          Payload        |
Header   | Header   | Argument 1 | Argument n |
```

Each argument consists of type info and payload.

Type Info: 32bit field

| Bit        | Value      | Description               |
|------------|------------|---------------------------|
|     0-3    |            | Type Length (TYLE)        |
|            |   0x00     | not defined               |
|            |   0x01     | 8 bit                     |
|            |   0x02     | 16 bit                    |
|            |   0x03     | 32 bit                    |
|            |   0x04     | 64 bit                    |
|            |   0x05     | 128 bit                   |
|            |  0x06–0x07 | reserved                  |
|      4     |            | Type Bool (BOOL)          |
|      5     |            | Type Signed (SINT)        |
|      6     |            | Type Unsigned (UINT)      |
|      7     |            | Type Float (FLOA)         |
|      8     |            | Type Array (ARAY)         |
|      9     |            | Type String (STRG)        |
|     10     |            | Type Raw (RAWD)           |
|     11     |            | Variable Info (VARI)      |
|     12     |            | Fixed Point (FIXP)        |
|     13     |            | Trace Info (TRAI)         |
|     14     |            | Type Struct (STRU)        |
|    15–17   |            | String Coding (SCOD)      |
|            |  0x00      | ASCII                     |
|            |  0x01      | UTF-8                     |
|            |  0x02-0x07 | reserved                  |
|    18–31   |            | reserved for future use   |


*Please notice that the discussed content is just an extract of the most
important fields that is required to parse the DLT files.*
