#!/usr/bin/env python3
"""
ActiveMQ Message Producer
A Python application to send messages to a classic ActiveMQ V5 queue.
"""

import sys

# Check Python version before importing other modules
if sys.version_info < (3, 6):
    sys.stderr.write("Error: This script requires Python 3.6 or higher.\n")
    sys.stderr.write(f"You are using Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\n")
    sys.stderr.write("Please run with 'python3' instead of 'python':\n")
    sys.stderr.write("  python3 activemq_producer.py [arguments]\n")
    sys.exit(1)

import argparse
import json
import random
import string
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional

import stomp


class MessageGenerator:
    """Generates message content in JSON or XML format."""
    
    @staticmethod
    def generate_random_string(length: int) -> str:
        """Generate a random string of specified length."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def generate_json_message(size_bytes: int) -> str:
        """Generate a JSON message of approximately the specified size."""
        # Calculate how much content we need for the desired size
        base_message = {
            "timestamp": datetime.utcnow().isoformat(),
            "message_id": str(random.randint(100000, 999999)),
            "type": "test_message",
            "data": ""
        }
        
        # Convert to JSON to calculate overhead
        base_json = json.dumps(base_message)
        overhead = len(base_json.encode('utf-8'))
        
        # Calculate remaining size needed for data field
        remaining_size = max(0, size_bytes - overhead - 10)  # 10 bytes buffer for quotes/formatting
        
        # Generate random data to fill the message
        if remaining_size > 0:
            base_message["data"] = MessageGenerator.generate_random_string(remaining_size)
        
        return json.dumps(base_message, indent=2)
    
    @staticmethod
    def generate_xml_message(size_bytes: int) -> str:
        """Generate an XML message of approximately the specified size."""
        root = ET.Element("message")
        
        # Add basic fields
        timestamp_elem = ET.SubElement(root, "timestamp")
        timestamp_elem.text = datetime.utcnow().isoformat()
        
        message_id_elem = ET.SubElement(root, "message_id")
        message_id_elem.text = str(random.randint(100000, 999999))
        
        type_elem = ET.SubElement(root, "type")
        type_elem.text = "test_message"
        
        data_elem = ET.SubElement(root, "data")
        
        # Calculate overhead
        xml_str = ET.tostring(root, encoding='unicode')
        overhead = len(xml_str.encode('utf-8'))
        
        # Calculate remaining size needed for data field
        remaining_size = max(0, size_bytes - overhead - 20)  # 20 bytes buffer
        
        # Generate random data to fill the message
        if remaining_size > 0:
            data_elem.text = MessageGenerator.generate_random_string(remaining_size)
        
        return ET.tostring(root, encoding='unicode')


class ActiveMQProducer:
    """Handles connection and message sending to ActiveMQ."""
    
    def __init__(self, host: str = 'localhost', port: int = 61613, username: Optional[str] = None, password: Optional[str] = None):
        """Initialize ActiveMQ producer."""
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
    
    def connect(self):
        """Establish connection to ActiveMQ."""
        try:
            self.connection = stomp.Connection([(self.host, self.port)])
            
            if self.username and self.password:
                self.connection.connect(self.username, self.password, wait=True)
            else:
                self.connection.connect(wait=True)
            
            print(f"✓ Connected to ActiveMQ at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"✗ Failed to connect to ActiveMQ: {e}", file=sys.stderr)
            return False
    
    def disconnect(self):
        """Disconnect from ActiveMQ."""
        if self.connection:
            try:
                self.connection.disconnect()
                print("✓ Disconnected from ActiveMQ")
            except Exception as e:
                print(f"Warning: Error during disconnect: {e}", file=sys.stderr)
    
    def send_message(self, queue_name: str, message: str, content_type: str = 'application/json'):
        """Send a message to the specified queue."""
        try:
            headers = {
                'content-type': content_type,
                'persistent': 'true'
            }
            self.connection.send(destination=f'/queue/{queue_name}', body=message, headers=headers)
            return True
        except Exception as e:
            print(f"✗ Failed to send message: {e}", file=sys.stderr)
            return False


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Send messages to a classic ActiveMQ V5 queue',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # ActiveMQ connection parameters
    parser.add_argument('--host', type=str, default='localhost',
                        help='ActiveMQ host')
    parser.add_argument('--port', type=int, default=61613,
                        help='ActiveMQ STOMP port')
    parser.add_argument('--username', type=str, default=None,
                        help='ActiveMQ username (optional)')
    parser.add_argument('--password', type=str, default=None,
                        help='ActiveMQ password (optional)')
    
    # Message parameters
    parser.add_argument('--queue', type=str, required=True,
                        help='Queue name to send messages to')
    parser.add_argument('--count', type=int, default=10,
                        help='Number of messages to send')
    parser.add_argument('--size', type=int, default=1024,
                        help='Approximate size of each message in bytes')
    parser.add_argument('--rate', type=float, default=1.0,
                        help='Message send rate (messages per second)')
    parser.add_argument('--format', type=str, choices=['json', 'xml'], default='json',
                        help='Message format (json or xml)')
    
    return parser.parse_args()


def main():
    """Main function to run the message producer."""
    args = parse_arguments()
    
    print("=" * 60)
    print("ActiveMQ Message Producer")
    print("=" * 60)
    print(f"Configuration:")
    print(f"  Host:     {args.host}:{args.port}")
    print(f"  Queue:    {args.queue}")
    print(f"  Count:    {args.count} messages")
    print(f"  Size:     {args.size} bytes")
    print(f"  Rate:     {args.rate} msg/sec")
    print(f"  Format:   {args.format.upper()}")
    print("=" * 60)
    
    # Create producer
    producer = ActiveMQProducer(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password
    )
    
    # Connect to ActiveMQ
    if not producer.connect():
        sys.exit(1)
    
    try:
        # Calculate delay between messages based on rate
        delay = 1.0 / args.rate if args.rate > 0 else 0
        
        # Determine content type
        content_type = 'application/json' if args.format == 'json' else 'application/xml'
        
        # Send messages
        sent_count = 0
        failed_count = 0
        start_time = time.time()
        
        for i in range(args.count):
            # Generate message
            if args.format == 'json':
                message = MessageGenerator.generate_json_message(args.size)
            else:
                message = MessageGenerator.generate_xml_message(args.size)
            
            # Send message
            if producer.send_message(args.queue, message, content_type):
                sent_count += 1
                print(f"[{sent_count}/{args.count}] Sent message ({len(message.encode('utf-8'))} bytes)")
            else:
                failed_count += 1
            
            # Rate limiting
            if delay > 0 and i < args.count - 1:
                time.sleep(delay)
        
        # Summary
        elapsed_time = time.time() - start_time
        print("=" * 60)
        print(f"Summary:")
        print(f"  Messages sent:     {sent_count}")
        print(f"  Messages failed:   {failed_count}")
        print(f"  Total time:        {elapsed_time:.2f} seconds")
        print(f"  Actual rate:       {sent_count / elapsed_time:.2f} msg/sec")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n✗ Interrupted by user")
    finally:
        producer.disconnect()


if __name__ == '__main__':
    main()
