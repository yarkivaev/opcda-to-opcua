# OPC-DA to OPC-UA Bridge

Bridge between OPC-DA (Classic) and OPC-UA servers.

## Requirements

- Python 3.4+
- Windows XP or later (for OPC-DA)
- OpenOPC library
- python-opcua library

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m opcda_to_opcua.app.main --da-progid "Vendor.OPC.Server"
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--da-host` | localhost | OPC-DA server hostname |
| `--da-progid` | (required) | OPC-DA server ProgID |
| `--ua-endpoint` | opc.tcp://0.0.0.0:4840 | OPC-UA endpoint |
| `--ua-uri` | http://example.org/opcda-bridge | Namespace URI |
| `--interval` | 500 | Polling interval (ms) |
| `--readonly` | false | Disable write-back |

## Development

### Run Tests (Docker)

```bash
docker build -t opcda-to-opcua-dev .
docker run --rm opcda-to-opcua-dev
```

### Check Coverage

```bash
docker run --rm opcda-to-opcua-dev sh -c \
  "coverage run -m unittest discover tests && coverage report"
```

## Architecture

```
OPC-DA Server <---> [Bridge] <---> OPC-UA Clients
                       |
              +--------+--------+
              |                 |
         DaSource          UaTarget
              |                 |
       OpenOpcSource      OpcUaTarget
```

## License

MIT
