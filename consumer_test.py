from lxml import etree
import xml.etree.ElementTree as ElementTree
import pika
import time
from datetime import datetime
import logging
import sys
import os

# ip = "172.17.0.2"
ip = "rabbitmq-rabbitmq-1"
#!/usr/bin/env python
connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.160.51', 5672, '/', pika.PlainCredentials('user', 'password')))

# Create a channel
channel = connection.channel()

def on_message(unused_channel, unused_method_frame, unused_header_frame, body):
    # Process the received message
    lines = body.decode()
    doc = ElementTree.fromstring(lines)
    # Process the XML message as needed
    # For example, you can extract information from the XML message
    id = doc.find("id").text
    category = doc.find("category")
    name = doc.find("name")
    amount = doc.find("amount")
    # print(f"Received heartbeat: id: {id}, name: {name}, category: {category}, amount: {amount}")
    print(f"Received heartbeat: id: {id}, name: {name}, amount: {amount}")

# Start consuming messages from the 'heartbeat' queue
channel.basic_consume(queue='inventory', on_message_callback=on_message, auto_ack=True)

print(' [*] Waiting for heartbeat messages. To exit press CTRL+C')
channel.start_consuming()