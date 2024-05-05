from lxml import etree
import xml.etree.ElementTree as ElementTree
import pika
import time
from datetime import datetime
import logging
import sys
import os

# ip = "172.17.0.2"
ip = "rabbitmq"
#!/usr/bin/env python
def main():
    credentials = pika.PlainCredentials('guest', 'guest')  # Placeholder for credentials
    connection = pika.BlockingConnection(pika.ConnectionParameters(ip, 5672, '/', credentials))
    channel = connection.channel()

    channel.queue_declare(queue='heartbeat', durable=True)

    def on_message(unused_channel, unused_method_frame, unused_header_frame, body):
        # Process the received message
        lines = body.decode()
        doc = ElementTree.fromstring(lines)
        # Process the XML message as needed
        # For example, you can extract information from the XML message
        id = doc.find("id").text
        name = doc.find("name").text
        category = doc.find("category").text
        amount = doc.find("amount").text
        location= doc.find("location").text
        amount_in_stock=doc.find("amount_in_stock").text
        # print(f"Received heartbeat: id: {id}, name: {name}, category: {category}, amount: {amount}")
        print(f"Received heartbeat: id: {id}, name: {name}, category: {category}, amount: {amount}, location:{location},amount in stock:{amount_in_stock}")

    # Start consuming messages from the 'heartbeat' queue
    channel.basic_consume(queue='heartbeat', on_message_callback=on_message, auto_ack=True)

    print(' [*] Waiting for heartbeat messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
