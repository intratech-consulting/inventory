import lxml
from lxml import etree
import pika
from datetime import datetime
from . import constants
import datetime
import requests
import json
import logging

# import xml.etree.ElementTree as ET

# Create a logger
logger = logging.getLogger("INFO")
logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG

# Define the log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Set the console logging level to INFO
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)

IP=constants.IP

HEADERS={
    'Content-Type': 'application/json',
    'Authorization': 'Basic YWRtaW46ZWhiMTIz',
    'Cookie': 'csrftoken=cDqCDkdERE2HS5d6AeavIFtzBmq9AW6k; sessionid=yxqgwt1c562bdis3d6mxlxez4ihrl4gi'
}

UID_HEADERS={
    'Content-type':'application/json', 
    'Accept':'application/json'
    }

def log_to_controller_room(function_name,msg,error,time):
    SYSTEM="inventory"

    if error==True:
        error='true'
    elif error==False:
        error='false'
    else:
        logger.info("Error must be boolean")

    Loggin_xml = f"""
    <LogEntry>
        <SystemName>{SYSTEM}</SystemName>
        <FunctionName>{function_name}</FunctionName>
        <Logs>{msg}</Logs>
        <Error>{error}</Error>
        <Timestamp>{time.isoformat()}</Timestamp>
    </LogEntry>
    """
    # Define your XML and XSD as strings


    Loggin_xsd = """
    <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
        <xs:element name="LogEntry">
            <xs:complexType>
                <xs:sequence>
                    <xs:element name="SystemName" type="xs:string"/>
                    <xs:element name="FunctionName" type="xs:string"/>
                    <xs:element name="Logs" type="xs:string"/>
                    <xs:element name="Error" type="xs:boolean"/>
                    <xs:element name="Timestamp" type="xs:dateTime"/>
                </xs:sequence>
            </xs:complexType>
        </xs:element>
    </xs:schema>
    """

    # Parse the XSD document
    xsd_doc = etree.fromstring(Loggin_xsd.encode())

    # Create a schema object
    schema = etree.XMLSchema(xsd_doc)

    # Setup connection and channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(IP, 5672, '/', pika.PlainCredentials('user', 'password')))
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='Loggin_queue', durable=True)
    channel.queue_bind(exchange='amq.topic', queue='Loggin_queue', routing_key='logs')

    # Format the XML with the current timestamp
    # formatted_Loggin_xml = Loggin_xml.format(datetime.datetime.utcnow().isoformat())
    # formatted_Loggin_xml = Loggin_xml.format(datetime.utcnow().isoformat())

    # Parse the XML
    xml_doc = etree.fromstring(Loggin_xml.encode())

    logger.info(function_name)
    logger.info(msg)
    logger.info(error)
    # Validate the XML against the schema
    if schema.validate(xml_doc):
        logger.info('XML is valid')
        # Publish the message to the queue
        channel.basic_publish(exchange='amq.topic', routing_key='logs', body=Loggin_xml)
        print('Message sent')
    else:
        logger.info('XML is not valid')
    logger.info("----------------------------------------------------------")

    # if True:
    #     print('XML is valid')
    #     logger.info('XML is valid')
    #     # Publish the message to the queue
    #     channel.basic_publish(exchange='', routing_key='Loggin_queue', body=formatted_Loggin_xml)
    #     print('Message sent')
    #     logger.info('XML is not valid')
    # else:
    #     print('XML is not valid')
    #     logger.info('XML is not valid')

    # Close the connection
    connection.close()

def get_user(user_pk):
    url = f"http://{IP}:880/api/company/{user_pk}"
    return requests.request("GET", url, headers=HEADERS)

def get_users():
    url = f"http://{IP}:880/api/company/"
    return requests.request("GET", url, headers=HEADERS)
    
def remove_from_stock(primary_key,quantity,order_id):
    url = f"http://{IP}:880/api/stock/remove/"

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

    return requests.request("POST", url, headers=HEADERS, data=payload)

def get_one_from_stock(primary_key):
    url = f"http://{IP}:880/api/stock/{primary_key}/"
    payload = {}
    return requests.request("GET", url, headers=HEADERS, data=payload)

def create_user(user_name,phone,email,uid):
    url = f"http://{IP}:880/api/company/"
    payload = json.dumps(
            {
                "name": user_name,
                "phone": phone,
                "email": email,
                "description": uid,
                "currency": "EUR",
                "is_customer": True,
                "is_manufacturer": False,
                "is_supplier": False,
            }
        )
    return requests.request("POST", url, headers=HEADERS, data=payload)

def update_user(payload,user_pk):
    url = f"http://{IP}:880/api/company/{user_pk}/"
    return requests.request("PUT", url, headers=HEADERS, data=payload)
    

def delete_user(user_pk):
    url = f"http://{IP}:880/api/company/{user_pk}/"
    payload={}
    return requests.request("DELETE", url, headers=HEADERS, data=payload)
    

def get_pk_from_masterUuid(uid):
    #MasterUuid
    masterUuid_url = f"http://{IP}:6000/getServiceId"
    masterUuid_payload = json.dumps(
        {
            "MASTERUUID": f"{uid}",
            "Service": "inventory"
        }
    )
    print(f"uid: {uid}")

    try:
        response = requests.request("POST", masterUuid_url, headers=UID_HEADERS ,data=masterUuid_payload)
        if response.status_code!=200:
            error_message=f"something went wrong when accessing this uid:{uid}, status code was not 200: {response.text}"
            raise Exception(error_message)           
    except requests.exceptions.RequestException as e:
        error_message=f"something went wrong accessing {uid} - {str(e)}"
        raise Exception(error_message)

   
    data=response.json()
    user_pk=data['inventory']
    
    value_after_dot = user_pk.split('.')[1]
    print(value_after_dot)
    return(value_after_dot)

def create_user_masterUuid(user_pk):
    masterUuid_url = f"http://{IP}:6000/createMasterUuid"
    masterUuid_payload = json.dumps({
    "Service": "inventory",
    "ServiceId":f"u.{user_pk}"
    })

    try:
        response = requests.request("POST", masterUuid_url, headers=UID_HEADERS ,data=masterUuid_payload)
        print(response)
        if response.status_code!=201:
            error_message=f"something went wrong when creating a user with user_pk {user_pk}, status code was not 201: {response.text}"
            raise Exception(error_message)    
        return response.json()['MasterUuid']       
    except requests.exceptions.RequestException as e:
        error_message=f"something went wrong when creating a user with user_pk {user_pk} - {str(e)}"
        raise Exception(error_message)
    
def add_user_pk_to_masterUuid(user_pk, uid):
    #MasterUuid
    masterUuid_url = f"http://{IP}:6000/addServiceId"
    masterUuid_payload = json.dumps(
        {
            "MasterUuid": f"{uid}",
            "Service": "inventory",
            "ServiceId": f"u.{user_pk}"
        }
    )
    print(f"uid: {uid}")
    print(f"pk: {user_pk}")
    return requests.request("POST", masterUuid_url, headers=UID_HEADERS ,data=masterUuid_payload)

def delete_user_pk_in_masterUuid(uid):
    #MasterUuid
    masterUuid_url = f"http://{IP}:6000/updateServiceId"
    masterUuid_payload = json.dumps(
        {
            "MASTERUUID": f"{uid}",
            "Service": "inventory",
            "ServiceId": "NULL"
        }
    )
    print(f"uid: {uid}")
    print("Pk has been deleted")
    return requests.request("POST", masterUuid_url, headers=UID_HEADERS ,data=masterUuid_payload)

def create_category(category_name,parent_category_id = ""):
    url = f"{IP}880/api/part/category/"
    if parent_category_id == "":
        payload = json.dumps({
        "name":category_name
    })
    else:
        payload = json.dumps({
            "name":category_name,
            "parent": parent_category_id
        })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46ZWhiMTIz',
        'Cookie': 'csrftoken=cDqCDkdERE2HS5d6AeavIFtzBmq9AW6k; sessionid=yxqgwt1c562bdis3d6mxlxez4ihrl4gi'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def create_part(part_name, category_id):
    url = f"http://{IP}:880/api/part/"
    payload = json.dumps({
        "name":part_name,
        "category": category_id,
        "minimum_stock":1
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46ZWhiMTIz',
        'Cookie': 'csrftoken=cDqCDkdERE2HS5d6AeavIFtzBmq9AW6k; sessionid=yxqgwt1c562bdis3d6mxlxez4ihrl4gi'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def create_stock(part_id,quantity,purchase_prise):
    url = f"http://{IP}:880/api/stock/"
    payload = json.dumps({
        "part":part_id,
        "quantity": quantity,
        "purchase_price":purchase_prise,
        "purchase_price_currency":"EUR",
        "description":"xxx"
    })
    # currency best een ENUM
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic YWRtaW46ZWhiMTIz',
        'Cookie': 'csrftoken=cDqCDkdERE2HS5d6AeavIFtzBmq9AW6k; sessionid=yxqgwt1c562bdis3d6mxlxez4ihrl4gi'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def create_part_masterUuid(part_id):
    url = f"http://{IP}:6000/createMasterUuid"
    masterUuid_payload = json.dumps({
    "Service": "inventory",
    "ServiceId":f"p.{part_id}"
    })
    try:
        response = requests.request("POST", url, headers=UID_HEADERS ,data=masterUuid_payload)
        print(response)
        if response.status_code!=201:
            error_message=f" 201: {response.text}"
            raise Exception(error_message)    
        return response.json()['MasterUuid']       
    except requests.exceptions.RequestException as e:
        error_message=f" {str(e)}"
        raise Exception(error_message)

def apply_partUuid(Uuid, part_id, category_id: str, part_name: str):
    part_url = f"http://{IP}:880/api/part/{part_id}/"
    payload = json.dumps({
        "category": category_id,
        "minimum_stock": 1,
        "name": part_name,
        "description": f"{Uuid}"
    })
    response = requests.request("PUT", part_url, headers=HEADERS, data=payload)
    print(response)