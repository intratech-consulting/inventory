import pika
import xml.etree.ElementTree as ET
import requests
import json

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.160.51', 5672, '/', pika.PlainCredentials('user', 'password')))
channel = connection.channel()

# Declare the exchange
exchange_name = "amq.topic"
channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)

# Declare a queue
queue_name = "inventory"
channel.queue_declare(queue=queue_name, durable=True)

# Bind the queue to the exchange with routing key 'user.crm'
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='inventree.user.test')

print(' [*] Waiting for messages. To exit, press CTRL+C')

# Define a callback function to handle incoming messages
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    # Process the XML message
    root = ET.fromstring(body)
    first_name= root.find('first_name__c').text
    last_name= root.find('last_name__c').text
    email= root.find('email__c').text
    telephone= root.find('telephone__c').text
    addUser(first_name,last_name,email,telephone)

    # Extract product details and remove from stock
    # products = root.find('products')
    # for product in products.findall('product'):
    #     product_id = product.find('id').text
    #     quantity = int(product.find('amount').text)
    #     print(f"Removing {quantity} units of product ID {product_id} from stock...")
    #     removeItemFromStock(product_id, quantity)

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Function to remove items from stock via API call
def addUser(first_name,last_name,email,telephone):
    # url = f"http://10.2.160.51:880/api/stock/{primary_key}/"
    # payload = {}
    # headers = {
    #     'Cookie': 'csrftoken=U4f3aiFMtXqeenAz6du2wfmD9e5ymh1K; sessionid=fnoffjbzoqhv66k0n1zonlsjt0qoqrzj'
    # }
    # response = requests.request("GET", url, headers=headers, data=payload)
    # item_data = response.json()
    # current_quantity = item_data.get("quantity", 100)
    # if current_quantity - quantity < 1:
    #     print("The stock is empty")
    #     return

    url = "http://10.2.160.51:880/api/company/"
    payload = {
    "name": f"{first_name} {last_name}",
    "phone": f'{telephone}',  # Use telephone from 
    "email": f'{email}',  # Use email from 
    "currency": "EUR",  # Set the currency (e.g., Australian Dollar)
    "is_customer": True,  # Example boolean values (modify as needed)
    "is_manufacturer": False,
    "is_supplier": False
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46ZWhiMTIz',
        'Cookie': 'csrftoken=cDqCDkdERE2HS5d6AeavIFtzBmq9AW6k; sessionid=yxqgwt1c562bdis3d6mxlxez4ihrl4gi'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

# Consume messages from the queue
channel.basic_consume(queue=queue_name, on_message_callback=callback)

# Start consuming
channel.start_consuming()