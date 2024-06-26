import pika
import xml.etree.ElementTree as ET
import requests
import json
import datetime
import logging
import time
# from .utilities import API_calls
from utilities import API_calls
from utilities import functions
from utilities import constants
# Establish connection to RabbitMQ server
IP=constants.IP
connection = pika.BlockingConnection(pika.ConnectionParameters(IP, 5672, '/', pika.PlainCredentials('user', 'password')))
channel = connection.channel()

# Declare the exchange
exchange_name = "amq.topic"
channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)

# Declare queue and bind it to the exchange with routing key pattern
queue_name = 'inventory'

routing_keys=['user.crm','user.facturatie','user.frontend','user.kassa','user.mailing','user.planning','order.*']

channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='user.crm')
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='user.facturatie')
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='user.frontend')
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='user.kassa')
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='user.mailing')
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='product.kassa')

# channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_keys)
def get_categories():
    url = f"http://{IP}:880/api/part/category/"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46ZWhiMTIz',
        'Cookie': 'csrftoken=cDqCDkdERE2HS5d6AeavIFtzBmq9AW6k; sessionid=yxqgwt1c562bdis3d6mxlxez4ihrl4gi'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch categories: {response.status_code} {response.text}")

def get_category_id(category_name):
    categories = get_categories()
    category_dict = {category['name']: category['pk'] for category in categories}
    return category_dict.get(category_name, None)

time.sleep(10) ### kies interval ###
def callback(ch, method, properties, body):
    try:
        # Determine the publisher based on routing key
        if method.routing_key.endswith('#.inventory'):
            ch.basic_ack(delivery_tag=method.delivery_tag)
        elif method.routing_key.startswith('user'):
            
            print("Received user message:")
            process_user(body)
        elif method.routing_key.startswith('order'):
            print("Received order message:")
            process_order(body)
        elif method.routing_key.startswith('product'):
            print("Received product message:")
            process_product(body)
        # Acknowledge the message
        else:
            API_calls.log_to_controller_room('Uknown',"message was not a product, order or user",True,datetime.datetime.now())
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        error_message=f"Error processing message:\n{str(e)}"
        API_calls.log_to_controller_room('Processing Error', error_message, True, datetime.datetime.now())
        ch.basic_ack(delivery_tag=method.delivery_tag)

def process_product(body):
    try:
        product_xml = ET.fromstring(body)
        # Extract required fields
        uid = product_xml.find('id').text
        crud = product_xml.find('crud_operation').text
    except Exception as e:
        raise Exception(f"Error in XML parsing or field extraction of uid and CRUD:\n{str(e)}")
    
    try:
        if crud == "create":
            create_product(uid, product_xml)
        else:
            raise Exception(f"CRUD operation '{crud}' is invalid for product with uid: {uid}")
    except Exception as e:
        raise Exception(e)

def process_order(body):
    # Process order message
    print(body.decode())
    # Call the API to remove item from stock
    try:
        order_xml = ET.fromstring(body)
        order_id = order_xml.find('id').text
        product_uid = order_xml.find('products/product/product_id').text
        quantity = int(order_xml.find('products/product/amount').text)
    except Exception as e:
        raise Exception(f"Error in XML parsing or field extraction of order_id, product_id and quantity:\n{str(e)}")
    
    try:
        product_pk=API_calls.get_pk_from_masterUuid(product_uid)
    except Exception as e:
        error_message = f"Error accessing product_uid {product_uid}: {str(e)}"
        raise Exception(error_message)
    
    
    removeItemFromStock(product_pk, quantity, order_id)

def process_user(body):
    try:
        user_xml = ET.fromstring(body)
        # Extract required fields
        uid=user_xml.find('id').text
        crud=user_xml.find('crud_operation').text
    except Exception as e:
        raise Exception(f"Error in XML parsing or field extraction of uid and CRUD:\n{str(e)}")
    

    try:
        if crud == "create":
            create_user(uid, user_xml)
        elif crud == "update":
            update_user(uid, user_xml)
        elif crud == "delete":
            if user_xml.find('routing_key').text!="user.facturatie":
                raise Exception(f"Delete request was not send by facturatie")
            else:
                delete_user(uid)
        else:
            raise Exception(f"CRUD was invalid for user with uid:{uid} - ") #{str(e)}
    except Exception as e:
        raise Exception(e)
        
def removeItemFromStock(primary_key, quantity, order_id):
    response = API_calls.get_one_from_stock(primary_key)
    item_data = response.json()
    current_quantity = item_data.get("quantity", 100)
    if current_quantity - quantity < 1:
        error_message="Stock can't go bellow 0"
        raise Exception (error_message)
    
    try:
        response= API_calls.remove_from_stock(primary_key,quantity,order_id)
        if response.status_code==201:
            API_calls.log_to_controller_room('processing order message for remove in stock',f"order with id:{order_id} has been processed",False,datetime.datetime.now())
        else:
            raise Exception(f"Error with removing from stock in db with order id:{order_id} : {response.text}  - status_code {response.status_code}")
            # API_calls.log_to_controller_room('processing order message for remove in stock',f"something went wrong when processing order with id:{order_id}",True,datetime.datetime.now())
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error with removing from stock with order id:{order_id} : {response.text} - status_code {response.status_code}")

#User operations
def create_user(uid, user_xml):
    try:        
        # Extract required fields
        first_name = user_xml.find('first_name').text
        last_name = user_xml.find('last_name').text
        phone = user_xml.find('telephone').text
        email = user_xml.find('email').text
        uid=user_xml.find('id').text
    except AttributeError as e:
        error_message = f"Error extracting user fields for CREATE: {str(e)}"
        raise Exception(error_message)
    
    user_name = f"{first_name}.{last_name}"
    
    try:
        response = API_calls.create_user(user_name, phone, email, uid)
        if response.status_code != 201:
            error_message = f"Error creating user {uid} - Status code was not 201: : {response.json()}| status_code: {response.status_code}"
            raise Exception(error_message)
        
        data = response.json()
        user_pk = data['pk']
        
        response = API_calls.add_user_pk_to_masterUuid(user_pk, uid)
        if response.status_code != 200:
            API_calls.delete_user(user_pk)
            error_message = f"Error adding user uid: {uid} when creating adding pk to uid- Status code was not 200, user has been locally deleted| status_code: {response.status_code}"
            raise Exception(error_message)
        else:
            API_calls.log_to_controller_room("C_CREATE user",f"user {uid} has been successfully created",False,datetime.datetime.now())
    except requests.exceptions.RequestException as e:
        error_message = f"Error creating user {uid} - {str(e)}"
        raise Exception(error_message)

def update_user(uid, user_xml):
    print('1')
    try:
        user_pk=API_calls.get_pk_from_masterUuid(uid)
    except Exception as e:
        error_message = f"Error getting user {uid} when updating user: {str(e)}"
        raise Exception(error_message)

    try:
        # Extract required fields        
        payload=functions.payload_extracting_update_user(user_xml,user_pk)
        if payload==True:
            return
    except Exception as e:
        error_message = f"Error accessing {uid} when extracting the payload for update user - {str(e)}"
        raise Exception(error_message)
    
    try:
        response = API_calls.update_user(payload,user_pk)
        if response.status_code==200:
            API_calls.log_to_controller_room('C_UPDATE user',f"user with uid:{uid} has been updated",False,datetime.datetime.now())
        else:
            raise Exception(f"Error with updating user {uid}, did not receiver status_code 200: {response.json()}| status_code: {response.status_code}")
            # API_calls.log_to_controller_room('processing user message for update',f"something went wrong when updating user with uid:{uid}",True,datetime.datetime.now())
            # return
    except requests.exceptions.RequestException as e:
        error_message = f"Error updating user {uid} when updating in db - {str(e)}"
        raise Exception(error_message)

def delete_user(uid):
    try:
        user_pk=API_calls.get_pk_from_masterUuid(uid)
    except Exception as e:
        error_message = f"Error getting user {uid} when deleting: {str(e)}"
        raise Exception(error_message)
    
    try:
        response=API_calls.delete_user(user_pk)
        if response.status_code != 204:
            if response.status_code==404:
                error_message = f"Error deleting user {uid} - Status code was not 404: user does not exist"
                raise Exception(error_message)
            error_message = f"Error deleting user {uid} - Status code was not 204: {response.text}| status_code: {response.status_code}"
            raise Exception(error_message)
        else:
            API_calls.log_to_controller_room('C_DELETE user', f"user with uid:{uid} has been deleted", False, datetime.datetime.now())
    except requests.exceptions.RequestException as e:
        error_message = f"Error deleting user {uid} - {str(e)}"
        raise Exception(error_message)
    
    try:
        response=API_calls.delete_user_pk_in_masterUuid(uid)
        if response.status_code != 200:
            error_message = f"Error deleting user {uid} - Status code was not 204: {response.text}| status_code: {response.status_code}"
            raise Exception(error_message)
        else:
            API_calls.log_to_controller_room('C_DELETE user', f"uid:{uid} has been deleted", False, datetime.datetime.now())
        
    except Exception as e:
        error_message = f"Error accessing user {uid} when deleting: {str(e)}"
        raise Exception(error_message)

#Product operations
def create_product(uid, product_xml):
    try:
        name = product_xml.find('name').text
        price = product_xml.find('price').text
        amount = product_xml.find('amount').text
        category_name = product_xml.find('category').text
        btw = product_xml.find('btw').text

        # categorie id vinden op basis van categorie naam
        category_id = get_category_id(category_name)
        if category_id is None:
            raise Exception(f"Category '{category_name}' not found")
    except AttributeError as e:
        error_message = f"Error extracting product fields: {str(e)}"
        raise Exception(error_message)
    except Exception as e:
        raise Exception(e)

    try:
        part_id = create_part(name, category_id, uid)
        print(f"Product created with Part ID: {part_id}")
        API_calls.log_to_controller_room("Product Creation", f"Product with uid:{uid} created successfully with part ID: {part_id}", False, datetime.datetime.now())
        
        # Create stock using the part ID
        stock_response = API_calls.create_stock(part_id, amount, price)
        print(f'Stock has been added: {stock_response}')
    except Exception as e:
        error_message = f"Failed to create product with uid:{uid}: {str(e)}"
        API_calls.log_to_controller_room("Product Creation Error", error_message, True, datetime.datetime.now())
        raise Exception(error_message)

def create_part(part_name, category_id, description):
    url = f"http://{IP}:880/api/part/"
    payload = json.dumps({
        "name": part_name,
        "category": category_id,
        "minimum_stock": 1,
        "description": description,
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46ZWhiMTIz',
        'Cookie': 'csrftoken=cDqCDkdERE2HS5d6AeavIFtzBmq9AW6k; sessionid=yxqgwt1c562bdis3d6mxlxez4ihrl4gi'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_data = response.json()
    if response.status_code == 201:
        part_id = response_data.get('pk')
        return part_id
    else:
        raise Exception(f"Failed to create part: {response.text}")

def create_stock(part_id, quantity, purchase_price):
    url = f"http://{IP}:880/api/stock/"
    payload = json.dumps({
        "part": part_id,
        "quantity": quantity,
        "purchase_price": purchase_price,
        "purchase_price_currency": "EUR",
        "description": "xxx"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46ZWhiMTIz',
        'Cookie': 'csrftoken=cDqCDkdERE2HS5d6AeavIFtzBmq9AW6k; sessionid=yxqgwt1c562bdis3d6mxlxez4ihrl4gi'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text



# Consume messages from the queue
channel.basic_consume(queue=queue_name, on_message_callback=callback)
# Start consuming
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()