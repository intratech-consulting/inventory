import pika
import xml.etree.ElementTree as ET
import requests
import json
import datetime
import logging
# from .utilities import API_calls
from utilities import API_calls
# Establish connection to RabbitMQ server
IP="10.2.160.51"
connection = pika.BlockingConnection(pika.ConnectionParameters(IP, 5672, '/', pika.PlainCredentials('user', 'password')))
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
        try:
            process_user(body)
        except Exception as e:
            error_message= "Error processing user message:\n"+ str(e)
            API_calls.log_to_controller_room('processing user message',error_message,True,datetime.datetime.now())

    elif method.routing_key.startswith('order'):
        print("Received order message:")
        try:
            process_order(body)
        except Exception as e:
            error_message= "Error processing order message:\n"+ str(e)
            API_calls.log_to_controller_room('processing order message',error_message,True,datetime.datetime.now())
    # Acknowledge the message
    else:
        API_calls.log_to_controller_room('None',"message was not an order or user",True,datetime.datetime.now())
    ch.basic_ack(delivery_tag=method.delivery_tag)

def process_order(body):
    # Process order message
    print(body.decode())
    # Call the API to remove item from stock
    order_xml = ET.fromstring(body)
    order_id = order_xml.find('id').text
    product_id = order_xml.find('products/product/product_id').text
    quantity = int(order_xml.find('products/product/amount').text)
    removeItemFromStock(product_id, quantity, order_id)

def process_user(body):
    # Process user message
    print(body.decode())
    # Parse XML message
    try:
        user_xml = ET.fromstring(body)
        # Extract required fields
        first_name = user_xml.find('first_name').text
        last_name = user_xml.find('last_name').text
        phone = user_xml.find('telephone').text
        email = user_xml.find('email').text
        uid=user_xml.find('id').text
        crud=user_xml.find('crud_operation').text
    except Exception as e:
        raise Exception("error in XML parsing or field extraction")
    

    try:
        if crud == "create":
            create_user(first_name, last_name, phone, email, uid)
        elif crud == "update":
            update_user(first_name, last_name, phone, email, uid)
        elif crud == "delete":
            delete_user(uid)
        else:
            print("crud not found")
    except Exception as e:
        raise Exception("error in given CRUD")
    # def switchCase(crud):
    #     switcher = {
    #         "create":create_user(first_name, last_name, phone, email, uid),
    #         "update":update_user(first_name, last_name, phone, email, uid, user_pk),
    #         "delete":delete_user(user_pk),
    #     }
    # switchCase(crud)
    
def filter_users(uid):
    response = API_calls.get_users()
    data=response.json()
    for user in data:
        description=user["description"]
        if (description==uid):
            id=user["pk"]
            return id
        
def removeItemFromStock(primary_key, quantity, order_id):
    response = API_calls.get_one_from_stock(primary_key)
    item_data = response.json()
    current_quantity = item_data.get("quantity", 100)
    if current_quantity - quantity < 1:
        print("The stock is empty")
        return
    
    try:
        response= API_calls.remove_from_stock(primary_key,quantity,order_id)
        if response.status_code==200:
            API_calls.log_to_controller_room('processing order message for delete in stock',f"order with id:{order_id} has been processed",False,datetime.datetime.now())
        else:
            API_calls.log_to_controller_room('processing order message for delete in stock',f"something went wrong when processing order with id:{order_id}",True,datetime.datetime.now())
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error with deleting from stock with order id:{order_id}")

def create_user(first_name, last_name, phone, email, uid):
    user_name = f"{first_name} {last_name}"
    try:
        response = API_calls.create_user(user_name,phone,email,uid)
        if response.status_code==201:
            API_calls.log_to_controller_room('processing user message for create',f"user with uid:{uid} has been created",False,datetime.datetime.now())
        else:
            API_calls.log_to_controller_room('processing user message for create',f"something went wrong when creating user with uid:{uid}",True,datetime.datetime.now())
            return
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error with creating user {uid}")
    
    data=response.json()
    user_pk=data['pk']

    #MasterUuid
    
    try:
        response = API_calls.add_user_pk_to_masterUuid(user_pk,uid)
        if response.status_code!=200:
            API_calls.log_to_controller_room('processing user message for create',f"something went wrong when accessing this uid:{uid}",True,datetime.datetime.now())
            return
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error with accessing user uid: {uid}")
    
    print(response)

def update_user(first_name, last_name, phone, email, uid):
    user_name = f"{first_name} {last_name}"
    user_pk=API_calls.get_user_pk_from_masterUuid(uid)
    
    try:
        response = API_calls.update_user(user_name,phone,email,uid,user_pk)
        if response.status_code==200:
            API_calls.log_to_controller_room('processing user message for update',f"user with uid:{uid} has been updated",False,datetime.datetime.now())
        else:
            API_calls.log_to_controller_room('processing user message for update',f"something went wrong when updating user with uid:{uid}",True,datetime.datetime.now())
            return
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error with updating user {uid}")
    

    

def delete_user(uid):
    user_pk=API_calls.get_user_pk_from_masterUuid(uid)
    try:
        response=API_calls.delete_user(user_pk)
        if response.status_code==204:
            API_calls.log_to_controller_room('processing user message for delete',f"user with uid:{uid} has been deleted",False,datetime.datetime.now())
        else:
            API_calls.log_to_controller_room('processing user message for delete',f"something went wrong when deleting user with uid:{uid}",True,datetime.datetime.now())
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error with deleting user {uid}")
    
    

    
    


# Consume messages from the queue
channel.basic_consume(queue=queue_name, on_message_callback=callback)
# Start consuming
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()