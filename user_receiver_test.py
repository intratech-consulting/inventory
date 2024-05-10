import pika
import xml.etree.ElementTree as ET

def callback(ch, method, properties, body):
    print("Received message:")
    body = body.strip()  # Remove leading and trailing whitespace
    print(body.decode('utf-8'))  # Assuming the message is encoded in UTF-8

    # Parse XML message
    root = ET.fromstring(body)

    # Extract required fields
    first_name = root.find('.//first_name__c').text
    last_name = root.find('.//last_name__c').text
    email = root.find('.//email__c').text
    telephone = root.find('.//telephone__c').text

    print("First Name:", first_name)
    print("Last Name:", last_name)
    print("Email:", email)
    print("Telephone:", telephone)

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.160.51', 5672, '/', pika.PlainCredentials('user', 'password')))
channel = connection.channel()

# Declare the exchange
exchange_name = "amq.topic"
channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)

# Declare and bind a queue
queue_name = "inventory"
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key="user.crm")

# Set up the consumer
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()