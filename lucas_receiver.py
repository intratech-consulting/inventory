import pika
import xml.etree.ElementTree as ET

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.160.51', 5672, '/', pika.PlainCredentials('user', 'password')))
channel = connection.channel()

# Declare the exchange
exchange_name = "amq.topic"
channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)

# Declare queue and bind it to the exchange with routing key pattern
queue_name = 'inventory'
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='order.*')
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='user.*')

def callback(ch, method, properties, body):
    # Determine the publisher based on routing key
    if method.routing_key.startswith('order'):
        print("Received order message:")
        root = ET.fromstring(body)
    elif method.routing_key.startswith('inventree.user'):
        print("Received user message:")
        root = ET.fromstring(body)
    print(body.decode())
    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Consume messages from the queue
channel.basic_consume(queue=queue_name, on_message_callback=callback)
# Start consuming
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()