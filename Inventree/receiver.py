import pika
import xml.etree.ElementTree as ET
import html
import json
import requests

# RabbitMQ connection parameters
credentials = pika.PlainCredentials('user', 'password')
parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare the queue and get the queue name
queue_result = channel.queue_declare(queue='order', durable=True)
queue_name = queue_result.method.queue

def removeItemFromStock(primary_key, quantity, headers):
    url = f"http://inventree-server:8000/api/stock/{primary_key}/"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        item_data = response.json()
        current_quantity = item_data.get("quantity", 100)
        if current_quantity - quantity < 1:
            print("De stock is leeg")
            return
        
        url = "http://inventree-server:8000/api/stock/remove/"
        payload = {
            "items": [
                {
                    "batch": "string",
                    "packaging": "string",
                    "pk": primary_key,
                    "quantity": quantity,
                    "status": ""
                }
            ],
            "notes": "string"
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")

def callback(ch, method, properties, body):
    decoded_body = html.unescape(body.decode())
    root = ET.fromstring(decoded_body)

    order_elem = root.find('order')
    if order_elem is not None:
        order_id = order_elem.find('id').text
        user_id = order_elem.find('user_id').text
        company_id = order_elem.find('company_id').text
        total_price = order_elem.find('total_price').text
        status = order_elem.find('status').text

        products = []
        for product_elem in order_elem.findall('.//product'):
            product_id = product_elem.find('id').text
            name = product_elem.find('name').text
            price = product_elem.find('price').text
            amount = product_elem.find('amount').text
            category = product_elem.find('category').text
            total = product_elem.find('total').text
            total_ex_btw = product_elem.find('totalExBtw').text
            btw = product_elem.find('btw').text
            products.append({
                'id': product_id,
                'name': name,
                'price': price,
                'amount': amount,
                'category': category,
                'total': total,
                'total_ex_btw': total_ex_btw,
                'btw': btw
            })

        print('[x] Parsed order message:')
        print(f"Order ID: {order_id}")
        print(f"User ID: {user_id}")
        print(f"Company ID: {company_id}")
        print(f"Total Price: {total_price}")
        print(f"Status: {status}")
        print("Products:")
        for product in products:
            id = product['id']
            quantity = int(product['amount'])
            # Pass headers to removeItemFromStock function
            headers = {
                'Cookie': 'csrftoken=V2WgldExQx0XKqBh7VaEjKQAVdwv4HV2; sessionid=viptlrlxu6uqvfsmdebrqyh0f1n4kvk2',
                'Authorization': 'Basic bHVjYXM6cm9vdA==',
                'Content-Type': 'application/json'
            }
            removeItemFromStock(id, quantity, headers)

    ch.basic_ack(delivery_tag=method.delivery_tag)

# Set up basic consumer with the correct queue name and callback function
channel.basic_consume(on_message_callback=callback, queue=queue_name)
print(' [*] Waiting for order messages. To exit press CTRL+C')

# Start consuming messages
channel.start_consuming()
