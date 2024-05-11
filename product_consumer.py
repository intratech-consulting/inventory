import pika
import xml.etree.ElementTree as ET

def callback(ch, method, properties, body):
    # Parse the XML data received from the message body
    root = ET.fromstring(body)
    product_id = root.find('id').text
    product_name = root.find('name').text
    product_price = root.find('price').text
    product_amount = root.find('amount').text
    product_category = root.find('category').text
    product_total = root.find('total').text
    product_total_ex_btw = root.find('total_ex_btw').text
    product_btw = root.find('btw').text

    # Process the data as required
    print(f"Received order message:")
    print(f"Product ID: {product_id}")
    print(f"Product Name: {product_name}")
    print(f"Product Price: {product_price}")
    print(f"Product Amount: {product_amount}")
    print(f"Product Category: {product_category}")
    print(f"Total: {product_total}")
    print(f"Total Excluding VAT: {product_total_ex_btw}")
    print(f"VAT: {product_btw}")
    print("")

def consume_orders():
    # Establish connection to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.160.53', 5672, '/', pika.PlainCredentials('user', 'password')))
    channel = connection.channel()

    exchange_name = "amq.topic"
    channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)

    result = channel.queue_declare(queue='product_test', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='product.inventory')

    # Set up the consumer to consume from the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for order messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    consume_orders()