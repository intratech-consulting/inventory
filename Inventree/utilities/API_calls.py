import lxml
from lxml import etree
import pika
from datetime import datetime
import requests
import json
# import xml.etree.ElementTree as ET

IP="10.2.160.51"

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
    print (msg)

    Loggin_xml = f"""
    <LogEntry>
        <SystemName>{SYSTEM}</SystemName>
        <FunctionName>{function_name}</FunctionName>
        <Logs>{msg}</Logs>
        <Error>{error}</Error>
        <Timestamp>{time}</Timestamp>
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
    formatted_Loggin_xml = Loggin_xml.format(datetime.utcnow().isoformat())

    # Parse the XML
    xml_doc = etree.fromstring(formatted_Loggin_xml.encode())

    # Validate the XML against the schema
    if schema.validate(xml_doc):
        print('XML is valid')
        # Publish the message to the queue
        channel.basic_publish(exchange='', routing_key='Loggin_queue', body=formatted_Loggin_xml)
        print('Message sent')
    else:
        print('XML is not valid')

    # Close the connection
    connection.close()

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

    response = requests.request("POST", url, headers=HEADERS, data=payload)
    print(response.text)

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

def update_user(user_name,phone,email,uid,user_pk):
    url = f"http://{IP}:880/api/company/{user_pk}"
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
    response = requests.request("PUT", url, headers=HEADERS, data=payload)
    print(response.text)

def delete_user(user_pk):
    url = f"http://{IP}:880/api/company/{user_pk}/"
    payload={}
    response = requests.request("DELETE", url, headers=HEADERS, data=payload)
    print(response)

def get_user_pk_from_masterUuid(uid):
    #MasterUuid
    masterUuid_url = f"http://{IP}:6000/getServiceId"
    masterUuid_payload = json.dumps(
        {
            "MASTERUUID": f"{uid}",
            "Service": "inventory"
        }
    )
    print(f"uid: {uid}")
    response = requests.request("POST", masterUuid_url, headers=UID_HEADERS ,data=masterUuid_payload)
    data=response.json()
    user_pk=data['inventory']
    print(user_pk)
    return(user_pk)

def add_user_pk_to_masterUuid(user_pk, uid):
    #MasterUuid
    masterUuid_url = f"http://{IP}:6000/addServiceId"
    masterUuid_payload = json.dumps(
        {
            "MasterUuid": f"{uid}",
            "Service": "inventory",
            "ServiceId": f"{user_pk}"
        }
    )
    print(f"uid: {uid}")
    print(f"pk: {user_pk}")
    return requests.request("POST", masterUuid_url, headers=UID_HEADERS ,data=masterUuid_payload)