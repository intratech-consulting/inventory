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
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='user.crm')
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='user.facturatie')
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='user.frontend')
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='user.kassa')
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='user.mailing')
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='user.planning')

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
        # Acknowledge the message
        else:
            API_calls.log_to_controller_room('Uknown',"message was not an order or user",True,datetime.datetime.now())
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        error_message=f"Error processing message:\n{str(e)}"
        API_calls.log_to_controller_room('Processing Error', error_message, True, datetime.datetime.now())
        ch.basic_ack(delivery_tag=method.delivery_tag)

def process_order(body):
    # Process order message
    print(body.decode())
    # Call the API to remove item from stock
    try:
        order_xml = ET.fromstring(body)
        order_id = order_xml.find('id').text
        product_id = order_xml.find('products/product/product_id').text
        quantity = int(order_xml.find('products/product/amount').text)
    except Exception as e:
        raise Exception(f"Error in XML parsing or field extraction of order_id, product_id and quantity:\n{str(e)}")
    removeItemFromStock(product_id, quantity, order_id)

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
            delete_user(uid)
        else:
            raise Exception(f"CRUD was invalid for user with uid:{uid} - {str(e)}")
    except Exception as e:
        raise Exception(e)
    # def switchCase(crud):
    #     switcher = {
    #         "create":create_user(first_name, last_name, phone, email, uid),
    #         "update":update_user(first_name, last_name, phone, email, uid, user_pk),
    #         "delete":delete_user(user_pk),
    #     }
    # switchCase(crud)
    
# def filter_users(uid):
#     response = API_calls.get_users()
#     data=response.json()
#     for user in data:
#         description=user["description"]
#         if (description==uid):
#             id=user["pk"]
#             return id
        
def removeItemFromStock(primary_key, quantity, order_id):
    response = API_calls.get_one_from_stock(primary_key)
    item_data = response.json()
    current_quantity = item_data.get("quantity", 100)
    if current_quantity - quantity < 1:
        print("The stock is empty")
        return
    
    try:
        response= API_calls.remove_from_stock(primary_key,quantity,order_id)
        if response.status_code==201:
            API_calls.log_to_controller_room('processing order message for remove in stock',f"order with id:{order_id} has been processed",False,datetime.datetime.now())
        else:
            raise Exception(f"Error with removing from stock with order id:{order_id}")
            # API_calls.log_to_controller_room('processing order message for remove in stock',f"something went wrong when processing order with id:{order_id}",True,datetime.datetime.now())
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error with removing from stock with order id:{order_id}")

def create_user(uid, user_xml):
    try:        
        # Extract required fields
        first_name = user_xml.find('first_name').text
        last_name = user_xml.find('last_name').text
        phone = user_xml.find('telephone').text
        email = user_xml.find('email').text
        uid=user_xml.find('id').text
    except AttributeError as e:
        error_message = f"Error extracting user fields: {str(e)}"
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
            error_message = f"Error accessing user uid: {uid} - Status code was not 200, user has been locally deleted| status_code: {response.status_code}"
            raise Exception(error_message)
        else:
            API_calls.log_to_controller_room("Creating user",f"user {uid} has been successfully created",False,datetime.datetime.now())
    except requests.exceptions.RequestException as e:
        error_message = f"Error creating user {uid} - {str(e)}"
        raise Exception(error_message)

def update_user(uid, user_xml):
    print('1')
    try:
        user_pk=API_calls.get_user_pk_from_masterUuid(uid)
    except Exception as e:
        error_message = f"Error accessing user {uid}: {str(e)}"
        raise Exception(error_message)

    try:
        # Extract required fields        
        payload=functions.payload_extracting_update_user(user_xml,user_pk)
    except Exception as e:
        error_message = f"Error accessing {uid} - {str(e)}"
        raise Exception(error_message)
    
    try:
        response = API_calls.update_user(payload,user_pk)
        if response.status_code==200:
            API_calls.log_to_controller_room('Updating user',f"user with uid:{uid} has been updated",False,datetime.datetime.now())
        else:
            raise Exception(f"Error with updating user {uid}, did not receiver status_code 200: {response.json()}| status_code: {response.status_code}")
            # API_calls.log_to_controller_room('processing user message for update',f"something went wrong when updating user with uid:{uid}",True,datetime.datetime.now())
            # return
    except requests.exceptions.RequestException as e:
        error_message = f"Error updating user {uid} - {str(e)}"
        raise Exception(error_message)
    

    

def delete_user(uid):
    try:
        user_pk=API_calls.get_user_pk_from_masterUuid(uid)
    except Exception as e:
        error_message = f"Error accessing user {uid}: {str(e)}"
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
            API_calls.log_to_controller_room('Deleting user', f"user with uid:{uid} has been deleted", False, datetime.datetime.now())
    except requests.exceptions.RequestException as e:
        error_message = f"Error deleting user {uid} - {str(e)}"
        raise Exception(error_message)
    
    try:
        API_calls.delete_user_pk_in_masterUuid(uid)
    except Exception as e:
        error_message = f"Error accessing user {uid}: {str(e)}"
        raise Exception(error_message)

 


# Consume messages from the queue
channel.basic_consume(queue=queue_name, on_message_callback=callback)
# Start consuming
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()