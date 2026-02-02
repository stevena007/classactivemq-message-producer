#!/usr/bin/env python3
"""
Demo script to show the message producer functionality without requiring ActiveMQ.
This simulates the message generation and display.
"""

import sys
import time
from activemq_producer import MessageGenerator

def demo_message_producer():
    """Demonstrate message producer functionality."""
    print("=" * 70)
    print("ActiveMQ Message Producer - DEMO MODE")
    print("(Simulating message generation without ActiveMQ connection)")
    print("=" * 70)
    
    configs = [
        {"format": "json", "count": 5, "size": 512, "rate": 2.0},
        {"format": "xml", "count": 3, "size": 256, "rate": 1.0},
    ]
    
    for config in configs:
        print(f"\n{'='*70}")
        print(f"Configuration: {config['count']} {config['format'].upper()} messages")
        print(f"Size: {config['size']} bytes, Rate: {config['rate']} msg/sec")
        print(f"{'='*70}\n")
        
        delay = 1.0 / config['rate']
        
        for i in range(config['count']):
            # Generate message
            if config['format'] == 'json':
                message = MessageGenerator.generate_json_message(config['size'])
            else:
                message = MessageGenerator.generate_xml_message(config['size'])
            
            actual_size = len(message.encode('utf-8'))
            print(f"[{i+1}/{config['count']}] Generated {config['format'].upper()} message ({actual_size} bytes)")
            
            # Show first message content
            if i == 0:
                preview = message[:150] + "..." if len(message) > 150 else message
                print(f"  Preview: {preview}")
            
            # Simulate delay
            if i < config['count'] - 1:
                time.sleep(delay)
    
    print(f"\n{'='*70}")
    print("Demo completed successfully!")
    print("To send messages to a real ActiveMQ instance, use:")
    print("  python activemq_producer.py --queue myQueue --count 10")
    print("=" * 70)

if __name__ == '__main__':
    demo_message_producer()
