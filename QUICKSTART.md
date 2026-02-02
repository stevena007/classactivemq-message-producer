# Quick Reference Card - ActiveMQ Message Producer

## Installation
```bash
pip install -r requirements.txt
```

## Basic Usage
```bash
python activemq_producer.py --queue <QUEUE_NAME>
```

## Common Examples

### Send 100 JSON messages at 10 msg/sec
```bash
python activemq_producer.py --queue myQueue --count 100 --rate 10 --format json
```

### Send large XML messages (5KB each)
```bash
python activemq_producer.py --queue xmlQueue --size 5120 --format xml
```

### Connect to remote ActiveMQ with auth
```bash
python activemq_producer.py \
  --host activemq.example.com \
  --username admin \
  --password secret \
  --queue remoteQueue
```

### Send slowly (1 msg every 5 seconds)
```bash
python activemq_producer.py --queue slowQueue --rate 0.2
```

## All Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--host` | localhost | ActiveMQ host |
| `--port` | 61613 | STOMP port |
| `--username` | None | Username (optional) |
| `--password` | None | Password (optional) |
| `--queue` | *required* | Queue name |
| `--count` | 10 | Number of messages |
| `--size` | 1024 | Message size (bytes) |
| `--rate` | 1.0 | Messages per second |
| `--format` | json | Message format (json/xml) |

## Test Without ActiveMQ
```bash
python demo.py
```

## Get Help
```bash
python activemq_producer.py --help
```
