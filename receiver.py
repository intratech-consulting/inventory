import pika
import xml.etree.ElementTree as ET
import html
import requests
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-container'))
channel = connection.channel()

queue = channel.queue_declare('order_notify', durable=True)
queue_name = queue.method.queue

channel.queue_bind(exchange='order', queue=queue_name, routing_key='order.notify')


def callback(ch, method, properties, body):
    decoded_body = html.unescape(body.decode())  # Decode HTML entities
    root = ET.fromstring(decoded_body)

    order_elem = root.find('order')  # Find the <order> element

    order_id = order_elem.find('id').text if order_elem.find('id') is not None else None
    user_id = order_elem.find('user_id').text if order_elem.find('user_id') is not None else None
    company_id = order_elem.find('company_id').text if order_elem.find('company_id') is not None else None
    total_price = order_elem.find('total_price').text if order_elem.find('total_price') is not None else None
    status = order_elem.find('status').text if order_elem.find('status') is not None else None

    products = []
    for product_elem in order_elem.findall('.//product'):
        product_id = product_elem.find('id').text if product_elem.find('id') is not None else None
        name = product_elem.find('name').text if product_elem.find('name') is not None else None
        price = product_elem.find('price').text if product_elem.find('price') is not None else None
        amount = product_elem.find('amount').text if product_elem.find('amount') is not None else None
        category = product_elem.find('category').text if product_elem.find('category') is not None else None
        total = product_elem.find('total').text if product_elem.find('total') is not None else None
        total_ex_btw = product_elem.find('totalExBtw').text if product_elem.find('totalExBtw') is not None else None
        btw = product_elem.find('btw').text if product_elem.find('btw') is not None else None

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
        print(
            f"  - ID: {product['id']}, Name: {product['name']}, Price: {product['price']}, Amount: {product['amount']}, Category: {product['category']}")

    # Call API functions to update stock
    for product in products:
        primary_key = int(product['id'])
        quantity = int(product['amount'])
        removeItemFromStock(primary_key, quantity)

    ch.basic_ack(delivery_tag=method.delivery_tag)


def removeItemFromStock(primary_key, quantity):
    url = f"http://inventree-server:80/api/stock/{primary_key}/"
    payload = {}
    headers = {
        'Cookie': 'csrftoken=V2WgldExQx0XKqBh7VaEjKQAVdwv4HV2; sessionid=i22fu7yg5jz1oe5t75o229v2ee5tzmdk'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    item_data = response.json()
    current_quantity = item_data["quantity"]
    # Check dat quantity niet onder 1 gaat
    if current_quantity - quantity < 1:
        print("De stock is leeg")
        return

    url = "http://inventree-server:80/api/stock/remove/"
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
        "notes": "string"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic cm9vdDpUZXN0V2FjaHR3b29yZDEu',
        'Cookie': 'csrftoken=V2WgldExQx0XKqBh7VaEjKQAVdwv4HV2; sessionid=i22fu7yg5jz1oe5t75o229v2ee5tzmdk'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def stockIdList():
    # Function to list stock items, similar to addItemToStock
    pass


channel.basic_consume(on_message_callback=callback, queue=queue_name)
print(' [*] Waiting for order messages. To exit press CTRL+C')

channel.start_consuming()