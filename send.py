#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('guest', 'guest')  # Placeholder for credentials
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
channel = connection.channel()

channel.queue_declare(queue='heartbeat', durable=True)

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()