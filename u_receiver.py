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

# Declare queue and bind it to the exchange with routing key pattern
queue_name = 'inventory'
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='order.*')
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='user.*')

def callback(ch, method, properties, body):
    # Determine the publisher based on routing key
    if method.routing_key.startswith('user'):
        print("Received user message:")
        process_user(body)

    elif method.routing_key.startswith('order'):
        print("Received order message:")
        process_order(body)
    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

def process_order(body):
    # Process order message
    print(body.decode())
    # Call the API to remove item from stock
    order_xml = ET.fromstring(body)
    order_id = order_xml.find('id').text
    product_id = order_xml.find('products/product/id').text
    quantity = int(order_xml.find('products/product/amount').text)
    removeItemFromStock(product_id, quantity, order_id)

def process_user(body):
    # Process user message
    print(body.decode())
    # Parse XML message
    user_xml = ET.fromstring(body)
    # Extract required fields
    first_name = user_xml.find('first_name').text
    last_name = user_xml.find('last_name').text
    phone = user_xml.find('telephone').text
    email = user_xml.find('email').text
    # Call the API to create a company
    createCompany(first_name, last_name, phone, email)


def removeItemFromStock(primary_key, quantity, order_id):
    url = f"http://10.2.160.51:880/api/stock/{primary_key}/"
    payload = {}
    headers = {
        'Cookie': 'csrftoken=U4f3aiFMtXqeenAz6du2wfmD9e5ymh1K; sessionid=fnoffjbzoqhv66k0n1zonlsjt0qoqrzj'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    item_data = response.json()
    current_quantity = item_data.get("quantity", 100)
    if current_quantity - quantity < 1:
        print("The stock is empty")
        return

    url = "http://10.2.160.51:880/api/stock/remove/"
    payload = json.dumps({
        "items": [
            {
                "batch": "string",
                "packaging": "string",
                "pk": primary_key,
                "quantity": f"{quantity}",
                "status": ""
            }
        ],
        "notes": order_id
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46ZWhiMTIz',
        'Cookie': 'csrftoken=cDqCDkdERE2HS5d6AeavIFtzBmq9AW6k; sessionid=yxqgwt1c562bdis3d6mxlxez4ihrl4gi'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def createCompany(first_name, last_name, phone, email):
    company_name = f"{first_name} {last_name}"
    url = "http://10.2.160.51:880/api/company/"
    payload = json.dumps(
            {
                "name": company_name,
                "phone": phone,
                "email": email,
                "currency": "EUR",
                "is_customer": True,
                "is_manufacturer": False,
                "is_supplier": False,
            }
        )
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
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()