# ActiveMQ Message Producer

A Python application to send configurable messages to a classic ActiveMQ V5 queue.

## Features

- 📨 Send multiple messages to ActiveMQ queues
- 📊 Configure message count, size, and send rate
- 🔄 Support for JSON and XML message formats
- 🎲 Automatic generation of message content
- ⚙️ Flexible configuration via command-line arguments
- 🔌 Support for authenticated connections

## Requirements

- Python 3.6+
- ActiveMQ 5.x with STOMP protocol enabled (default port 61613)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/stevena007/classactivemq-message-producer.git
cd classactivemq-message-producer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Send 10 JSON messages to a queue:
```bash
python activemq_producer.py --queue myQueue
```

### Advanced Usage

```bash
python activemq_producer.py \
  --host localhost \
  --port 61613 \
  --queue testQueue \
  --count 100 \
  --size 2048 \
  --rate 5.0 \
  --format json
```

### Command-Line Arguments

| Argument | Description | Default | Required |
|----------|-------------|---------|----------|
| `--host` | ActiveMQ host | localhost | No |
| `--port` | ActiveMQ STOMP port | 61613 | No |
| `--username` | ActiveMQ username | None | No |
| `--password` | ActiveMQ password | None | No |
| `--queue` | Queue name to send messages to | - | **Yes** |
| `--count` | Number of messages to send | 10 | No |
| `--size` | Approximate size of each message in bytes | 1024 | No |
| `--rate` | Message send rate (messages per second) | 1.0 | No |
| `--format` | Message format: `json` or `xml` | json | No |

## Examples

### Send 50 XML messages at 10 messages/second
```bash
python activemq_producer.py --queue xmlQueue --count 50 --rate 10 --format xml
```

### Send large JSON messages (10KB each)
```bash
python activemq_producer.py --queue largeQueue --count 20 --size 10240 --format json
```

### Send to remote ActiveMQ with authentication
```bash
python activemq_producer.py \
  --host activemq.example.com \
  --port 61613 \
  --username admin \
  --password secret \
  --queue remoteQueue \
  --count 100
```

### Send messages slowly (1 message every 2 seconds)
```bash
python activemq_producer.py --queue slowQueue --count 10 --rate 0.5
```

## Message Format

### JSON Format
Messages are generated with the following structure:
```json
{
  "timestamp": "2026-02-02T04:34:50.123456",
  "message_id": "123456",
  "type": "test_message",
  "data": "random_content_to_fill_size..."
}
```

### XML Format
Messages are generated with the following structure:
```xml
<message>
  <timestamp>2026-02-02T04:34:50.123456</timestamp>
  <message_id>123456</message_id>
  <type>test_message</type>
  <data>random_content_to_fill_size...</data>
</message>
```

## Running ActiveMQ Locally

If you need to test with a local ActiveMQ instance:

```bash
# Using Docker
docker run -d --name activemq \
  -p 61616:61616 \
  -p 8161:8161 \
  -p 61613:61613 \
  rmohr/activemq:5.15.9

# Access the web console at http://localhost:8161
# Default credentials: admin/admin
```

## Troubleshooting

### Connection refused
- Ensure ActiveMQ is running
- Verify the STOMP connector is enabled in ActiveMQ configuration
- Check that the host and port are correct

### Authentication failed
- Verify username and password are correct
- Check ActiveMQ security settings

### Message send failures
- Check queue permissions
- Verify disk space on ActiveMQ server
- Review ActiveMQ logs for errors

## License

MIT License