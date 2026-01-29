# OPC-DA to MQTT Publisher

Python library that reads tags from OPC-DA server and publishes them to MQTT broker.

## Requirements

- Python 2.7.9
- Windows XP (for production with OpenOPC)
- OpenOPC 1.3.1
- paho-mqtt

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Using config.json

Copy `config.example.json` to `config.json` and edit:

```bash
cp config.example.json config.json
python -m opcda_to_mqtt.app.main
```

### Using CLI arguments

```bash
python -m opcda_to_mqtt.app.main \
  --da-progid "OPCDataStore.TOPCElemerServer.2" \
  --mqtt-host "192.168.1.100" \
  --mqtt-topic "factory/line1" \
  --prefix "COM1"
```

CLI arguments override config.json values.

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--config` | config.json | Path to JSON configuration file |
| `--da-progid` | required | OPC-DA server ProgID |
| `--da-host` | localhost | OPC-DA server host |
| `--mqtt-host` | required | MQTT broker host |
| `--mqtt-port` | 1883 | MQTT broker port |
| `--mqtt-topic` | required | Base MQTT topic |
| `--prefix` | - | OPC tag prefix for discovery |
| `--tags` | - | Explicit tag list |
| `--interval` | 500 | Polling interval in milliseconds |
| `--workers` | 50 | Number of worker threads |

## MQTT Message Format

Topic: `{base_topic}/{tag_path}`

```json
{
  "value": 123.45,
  "quality": "good"
}
```

## Development

Run tests in Docker:

```bash
docker build -t opcda-mqtt-dev .
docker run --rm opcda-mqtt-dev
```

Check coverage:

```bash
docker run --rm opcda-mqtt-dev sh -c \
  "coverage run -m unittest discover tests && coverage report"
```

## License

MIT
